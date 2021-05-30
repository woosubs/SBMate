# sbmate.py
# calculate annotation scores

# import collections
import libsbml
import networkx as nx
import os
import pickle
import re
import requests
import constants as cn
import consistency_score as cs
import sbml_annotation as sa


class AnnotationMetrics(object):
  """
  Collect model annotations and
  calculate three scores:
  1. coverage
  2. consistency
  3. specificity
  """
  def __init__(self, model_file):
    """
    :param str model_file: address/name of the .xml model file
    """
    self.annotations = sa.SortedSBMLAnnotation(file=model_file)
    self.annotated_entities, self.coverage = self.getCoverage()
    self.consistent_entities, self.consistency = self.getConsistency(self.annotated_entities)
    #self.coverage = self.getCoverage()

  def getCoverage(self):
    """
    Coverage is defined as:
    (# annotated entities) / (# annotatable entities).
    :return str-list:
    :return float:
    """
    num_annotatable_entities = len(self.annotations.annotations)
    # list_annotated_entities is constructed as below =>
    # for key in self.annotations.annotations.keys():
    #   if any(self.annotations.annotations[key][ont] for ont in cn.KNOWLEDGE_TYPES_REP):
    #   	add key to the list
    list_annotated_entities = [k for \
                               k in \
                               self.annotations.annotations.keys() \
                               if any([self.annotations.annotations[k][ont] for ont \
                               in cn.KNOWLEDGE_TYPES_REP])]
    num_annotated_entities = len(list_annotated_entities)
    return list_annotated_entities, float(num_annotated_entities/num_annotatable_entities)

  def getConsistency(self, annotated_entities):
    """
    Consistency is defined as:
    (# consistently annotated entities) / (# annotated entities)
    'annotated_entities' is a list of annotated model entities.
    :param str-list annotated_entities:
    :return str-list/None: return None if no object is annotated
    :return float/None: return None if no object is annotated
    """
    # get annotated entities
    consistent_entities = []
    # k is the name of each model entity
    for k in annotated_entities:
      entity_annotation = self.annotations.annotations[k]
      entity_type = entity_annotation['object_type']
      annotated_knowledge_resources = [ont \
                                       for ont in cn.KNOWLEDGE_TYPES_REP \
                                       if entity_annotation[ont]]
      # By setup, annotated_knowledge_resources should have at least one item
      is_consistent_list = [cs.CONSISTENT_FUNC[one_ont](entity_annotation[one_ont], entity_type) \
                            for one_ont in annotated_knowledge_resources]
      if all(is_consistent_list):
        consistent_entities.append(k) 
    # if there is at least one annotated entity, return intended values
    if annotated_entities:
      return consistent_entities, float(len(consistent_entities) / len(annotated_entities))
    # else happens if no object is annotated
    else: 
      return None, None


























