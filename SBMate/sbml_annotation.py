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
  from sbo_term and getAnnotationString(). 
  """

  def __init__(self, input_file,
               select_objects=cn.BIOMODEL_OBJECTS):
    """
    :param str file: name/location of file
    :param set/tuple select_objects: objects to pull out annotation from
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
    Return None if term is not given
    :param sbml-object:sbml_object
    :return namedtuple 'ObjectAnnotation': (id, type, str/None)
    """
    def formatSBO(sbo_num):
      """
      Reformat an SBO term into str.
      Return None if -1 (not provided).
      :param int: sbo_num
      :return str/None:
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
    If neither exists, return None
    :param sbml-object:sbml_object
    :return namedtuple 'ObjectAnnotation': (id, type, str/None)
    """
    input_id = sbml_object.getId()
    input_type = type(sbml_object)
    input_annotation = sbml_object.getAnnotationString()
    #
    is_str = ''
    isVersionOf_str = ''
    is_str_match = re.findall('<bqbiol:is>.*?<\/bqbiol:is>',
                              input_annotation,
                              flags=re.DOTALL)
    if len(is_str_match)>0:
      is_str_match_filt = [s.replace("      ", "") for s in is_str_match]
      is_str = '\n'.join(is_str_match_filt)

    is_VersionOf_str_match = re.findall('<bqbiol:isVersionOf>.*?<\/bqbiol:isVersionOf>',
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
    :param str input_id:
    :return dict: {resource:identifier}
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
      m = re.search('[0-9]+', inp_sbo)
      if m:
        res_sbo = 'SBO:' + inp_sbo[m.start():m.end()]
        return res_sbo
      
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
    If nothing exists, return an empty string ''
    :param str input_annotation:
    :return list-str/None:
    """
    if input_annotation:
      identifiers_list = re.findall('identifiers\.org/.*/', input_annotation)
      return [(r.split('/')[1],r.split('/')[2].replace('\"', '')) \
              for r in identifiers_list \
              if r.split('/')[1] in cn.ALL_KNOWLEDGE_TYPES]
    else:
      return None