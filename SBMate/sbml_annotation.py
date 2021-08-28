# sbml_annotation.py

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
    def formatSBO(sbo_num):
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
    #
    input_id = sbml_object.getId()
    input_type = type(sbml_object)
    input_sbo = formatSBO(sbml_object.sbo_term)
    #
    return ObjectAnnotation(input_id, input_type, input_sbo)
    
  def getOntAnnotation(self, sbml_object):
    """
    Parse string and return string annotation,
    marked as <bqbiol:is> or <bqbiol:isVersionOf>.
    If neither exists, return None/

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

    is_VersionOf_str_match = re.findall('<bqbiol:isVersionOf[^a-zA-Z].*?<\/bqbiol:isVersionOf>',
                                        input_annotation,
                                        flags=re.DOTALL)
    #
    if len(is_VersionOf_str_match) > 0:
      is_VersionOf_str_match_filt = [s.replace("      ", "") for s in is_VersionOf_str_match]
      isVersionOf_str = '\n'.join(is_VersionOf_str_match_filt)
    #
    combined_str = is_str + isVersionOf_str
    if combined_str == '':
      combined_str = None
    return ObjectAnnotation(input_id, input_type, combined_str)



class SortedSBMLAnnotation(object):
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
    self.raw_annotations = RawSBMLAnnotation(input_file=file)
    self.object_ids = [ele.id for ele in self.raw_annotations.str_annotation]
    self.annotations = {one_id:self.getAnnotationDict(one_id) for one_id in self.object_ids}

  def getAnnotationDict(self, input_id):
    """
    Get dictionary of annotations for an object,
    where the key is object id
    and the items are each annotation
    per category. 
    Returns a nested dictionary
    for each object. 

    Parameters
    ----------
    input_id: str
        Model entity id (name) to get annotation of.

    Returns
    -------
    annotation_dict: dict {dict: {resource:identifier}}
        Nested dictionary of annotations per object. 
    """
    annotation_dict = dict.fromkeys(cn.KNOWLEDGE_TYPES_REP)
    str_annotation_item = [ele for ele in self.raw_annotations.str_annotation \
                           if ele.id==input_id][0]
    str_annotation_tuples = self.getKnowledgeResourceTuple(str_annotation_item.annotation)
    if str_annotation_tuples:
      tup_keys = list(set([cn.KNOWLEDGE_TYPES_DCT[ele[0]] for ele in str_annotation_tuples]))
      for one_key in tup_keys:
        vals = [ele[1] for ele in str_annotation_tuples if cn.KNOWLEDGE_TYPES_DCT[ele[0]]==one_key]
        annotation_dict[one_key] = vals
    
    # extra formatting for sbo
    def getSBOForm(inp_sbo):
      """
      Reformat an SBO term into str.
      Return None if -1 (not provided).

      Parameters
      ----------
      inp_sbo: int

      Returns
      -------
      res_sbo: str/None
          Return None if sbo term is -1 
          (i.e.,  not provided)
      """
      m = re.search('[0-9]+', inp_sbo)
      if m:
        res_sbo = 'SBO:' + inp_sbo[m.start():m.end()]
        return res_sbo
      else:
        return None
      
    if annotation_dict['sbo']:
      annotation_dict['sbo'] = [getSBOForm(ele) for ele in annotation_dict['sbo']]

    # get sbo term from .sbo_term
    sbo_item = [ele for ele in self.raw_annotations.sbo \
                if ele.id==input_id][0]
    if sbo_item.annotation:
      # check if sbo term is also given as string
      if annotation_dict['sbo']:
        annotation_dict['sbo'] = annotation_dict['sbo'].append(sbo_item.annotation)
      else:
        annotation_dict['sbo'] = [sbo_item.annotation]
    # finally, add the object id and type
    annotation_dict['object_id'] = input_id
    annotation_dict['object_type'] = str_annotation_item.object_type
    
    return annotation_dict

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
      identifiers_list = re.findall('identifiers\.org/.*/', input_annotation)
      return [(r.split('/')[1],r.split('/')[2].replace('\"', '')) \
              for r in identifiers_list \
              if r.split('/')[1] in cn.ALL_KNOWLEDGE_TYPES]
    else:
      return None







