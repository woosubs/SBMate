# sbml_annotation2.py
# updated versino of sbml_annotation.py

import collections
import libsbml
import os
import re
from SBMate import constants as cn

ObjectAnnotation = collections.namedtuple('ObjectAnnotation',
                                        ['id', 'object_type', 'annotation'],
                                        )


class RawSBMLAnnotation(object):
  """
  Collection of SBML object Annotations,
  from sbo_term and getAnnotationString() methods.

  Attributes
  ----------
  sbo: namedtuple 'ObjectAnnotation' - list
      Collection of SBO terms
  str_annotation: namedtuple 'ObjectAnnotation' - list
      Collection of string annotations,
      bqbiol:is or bqbiol:isVersionOf.

  Methods
  -------
  getSBOAnnotation (sbml_object)
      Create a list of SBO terms
      from .sbo_term attribute of
      libsbml model entity.
  getOntAnnotatoin (sbml_object)
      Create a list of string annotations
      from .getAnnotataionString(). method of
      libsbml model entity. 
  """

  def __init__(self, input_file,
               select_objects=cn.BIOMODEL_OBJECTS):
    """
    Parameters
    ----------
    input_file: str
        Name/location of model file (.xml)
    select_objects: libsbml.AutoProperty - list
        List of objects to pull out annotations from.
    """
    # load sbml file
    reader = libsbml.SBMLReader()
    document = reader.readSBML(input_file)
    # only keep the objects of interest
    model_objects = [ele for ele in document.getListOfAllElements() \
                     if isinstance(ele, tuple(select_objects))] 
    self.sbo = [self.getSBOAnnotation(ele) for ele in model_objects]
    self.str_annotation = [self.getOntAnnotation(ele) for ele in model_objects]

  def formatSBO(self, sbo_num):
    """
    Reformat an SBO term into str.
    Return None if -1 (not provided).

    Parameters
    ----------
    sbo_num: int

    Returns
    -------
    '': str/None
        Return None if sbo term is -1 
        (i.e.,  not provided)
    """
    if sbo_num == -1:
      return None
    else:
      return 'SBO:' + format(sbo_num, '07d')

  def getSBOAnnotation(self, sbml_object):
    """
    Returns a proper SBO term (e.g., SBO:0000290) 
    using the given sbml object.
    Return None if term is not given.

    Parameters
    ----------
    sbml_object: libsbml.AutoProperty

    Returns
    -------
    '': namedtuple 'ObjectAnnotation': (id, type, str/None)
    """
    input_id = sbml_object.getId()
    input_type = type(sbml_object)
    input_sbo = self.formatSBO(sbml_object.sbo_term)
    #
    return ObjectAnnotation(input_id, input_type, input_sbo)


  def getOntAnnotation(self, sbml_object):
    """
    Parse string and return string annotation,
    marked as <bqbiol:is> or <bqbiol:isVersionOf>.
    If neither exists, return None as annotation.

    Parameters
    ----------
    sbml_object: libsbml.AutoProperty

    Returns
    -------
    '': namedtuple 'ObjectAnnotation': (id, type, str/None)
    """
    input_id = sbml_object.getId()
    input_type = type(sbml_object)
    input_annotation = sbml_object.getAnnotationString()
    #
    is_str = ''
    isVersionOf_str = ''
    is_str_match = re.findall('<bqbiol:is[^a-zA-Z].*?<\/bqbiol:is>',
                              input_annotation,
                              flags=re.DOTALL)
    if len(is_str_match)>0:
      is_str_match_filt = [s.replace("      ", "") for s in is_str_match]
      is_str = '\n'.join(is_str_match_filt)

    isVersionOf_str_match = re.findall('<bqbiol:isVersionOf[^a-zA-Z].*?<\/bqbiol:isVersionOf>',
                                        input_annotation,
                                        flags=re.DOTALL)
    #
    if len(isVersionOf_str_match) > 0:
      is_VersionOf_str_match_filt = [s.replace("      ", "") for s in isVersionOf_str_match]
      isVersionOf_str = '\n'.join(is_VersionOf_str_match_filt)
    #
    combined_str = dict()
    if is_str_match:
      combined_str['is'] = is_str_match
    if isVersionOf_str_match:
      combined_str['isVersionOf'] = isVersionOf_str_match
    return ObjectAnnotation(input_id, input_type, combined_str)


class SBMLAnnotation(object):
  """
  SBML annotations sorted by type.
  SBO, GO, KEGG, CHEBI, UNIPROT. 

  Attributes
  ----------
  raw_annotations: RawSBMLAnnotation
      Instance of RawSBMLAnnotation class.
  object_ids: str-list
      Names of model entities. 
  annotations: dict(dict)
      Dictionary of dictionary. 
      object_id: {ontology type: identifiers}

  Methods
  -------
  getAnnotoationDict (input_id)
      Get dictionary of annotations.
  getKnowledgeResourceTuple (input_annotation)
      Extract identifiers from URI, 
      included in the string annotation. 
  """

  def __init__(self, file, knowledge_resources=cn.KNOWLEDGE_TYPES_REP):
    # For now, use default biomodel objects.
    self.raw_annotation = RawSBMLAnnotation(input_file=file)
    self.object_ids = [ele.id for ele in self.raw_annotation.str_annotation]
    self.annotation_by_qualifier = {one_id:self.getAnnotationDictByQualifier(one_id) for one_id in self.object_ids}
    self.annotations = {one_id:self.getAnnotationDictByOntology(self.annotation_by_qualifier[one_id]) for one_id in self.object_ids}

  def getAnnotationDictByQualifier(self, input_id):
    """
    Get dictionary of annotations for an object,
    where the key is ['is', 'isVersionOf']
    and the items are annotation tuples
    SBO term is treated as under 'is' qualifier.
    Dictionary indludes entity name & lisbsbml type. 

    Parameters
    ----------
    input_id: str
        Model entity id (name) to get annotation of.

    Returns
    -------
    annotation_dict_qualifier: dict qualifier: tuple
        Dictionary of annotations per type.
    """
    
    str_annotation_item = [ele for ele in self.raw_annotation.str_annotation \
                           if ele.id==input_id][0]
    annotation_dict_qualifier = {type_k:self.getKnowledgeResourceTuple(str_annotation_item.annotation[type_k]) \
                                 for type_k in str_annotation_item.annotation.keys()}
    # add SBO case
    sbo_item = [ele for ele in self.raw_annotation.sbo \
                if ele.id==input_id][0]
    if sbo_item.annotation:
      if 'is' in annotation_dict_qualifier.keys():
        annotation_dict_qualifier['is'].append(('sbo', sbo_item.annotation)) 
      else:
        annotation_dict_qualifier['is'] = [('sbo', sbo_item.annotation)]
    annotation_dict_qualifier['object_id'] = input_id
    annotation_dict_qualifier['object_type'] = str_annotation_item.object_type
    return annotation_dict_qualifier

  def getAnnotationDictByOntology(self, qualifier_dict):
    """
    Get dictionary of annotations for an object,
    for given knowledge resource type. 

    Parameters
    ----------
    qualifier_dict: dict
        Dictionary of qualifier: annotation tuple

    Returns
    -------
    qualifier_dict: dict ontology: tuple
        Dictionary of annotations per ontology.
    """
    # collect all tuples for each qualifier
    annotation_dict_ontology = dict.fromkeys(cn.KNOWLEDGE_TYPES_REP)
    valid_dict_keys = [one_k for one_k in qualifier_dict.keys() \
                       if one_k not in ['object_id', 'object_type']]
    if valid_dict_keys:
      all_tups = []
      for one_k in valid_dict_keys:
        all_tups = all_tups + qualifier_dict[one_k]
        tup_keys = list(set([cn.KNOWLEDGE_TYPES_DCT[ele[0]] for ele in all_tups]))
        for one_key in tup_keys:
          vals = [ele[1] for ele in all_tups if cn.KNOWLEDGE_TYPES_DCT[ele[0]]==one_key]
          annotation_dict_ontology[one_key] = vals
    # finally, add the object id and type
    annotation_dict_ontology['object_id'] = qualifier_dict['object_id']
    annotation_dict_ontology['object_type'] = qualifier_dict['object_type']
    #
    return annotation_dict_ontology

  def getKnowledgeResourceTuple(self, input_annotation):
    """
    Extract all annotation type tuple from URIs 
    marked with identifier.org.
    If nothing exists, return None

    Parameters
    ----------
    input_annotation: str
        Annotation string to extract annotation URI from.

    Returns
    -------
    '': str-tuple/None
        Extracted annotation.
        Ontology - identifier tuple.
    """
    if input_annotation:
      identifiers_list = re.findall('identifiers\.org/.*/', ''.join(input_annotation))
      return [(r.split('/')[1],r.split('/')[2].replace('\"', '')) \
              for r in identifiers_list \
              if r.split('/')[1] in cn.ALL_KNOWLEDGE_TYPES]
    else:
      return None




