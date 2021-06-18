# sbmate.py
# calculate annotation scores

import libsbml
import networkx as nx
import numpy as np
import os
import pickle
import pandas as pd
import re
import requests
from SBMate import constants as cn
from SBMate import consistency_score as cs
from SBMate import sbml_annotation as sa
from SBMate import specificity_score as ss

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
    (explain more on consistency, specificity etc.)
    """
    self.annotations = sa.SortedSBMLAnnotation(file=model_file)
    self.annotated_entities, self.coverage = self.getCoverage()
    self.consistent_entities, self.consistency = self.getConsistency(self.annotated_entities)
    self.specificity = self.getSpecificity(self.consistent_entities)

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
    if annotated_entities:
      consistent_entities = []
      # k is the name of each model entity
      for k in annotated_entities:
        entity_annotation = self.annotations.annotations[k]
        entity_type = entity_annotation['object_type']
        annotated_knowledge_resources = [ont \
                                         for ont in cn.KNOWLEDGE_TYPES_REP \
                                         if entity_annotation[ont]]
        # By setup, annotated_knowledge_resources should have at least one item
        is_consistent_list = [cs.CONSISTENCY_FUNC[one_ont](entity_annotation[one_ont], entity_type) \
                              for one_ont in annotated_knowledge_resources]
        if all(is_consistent_list):
          consistent_entities.append(k) 
      # if there is at least one annotated entity, return intended values
      return consistent_entities, float(len(consistent_entities) / len(annotated_entities))
    # else happens if no object is annotated
    else: 
      return None, None

  def getSpecificity(self, consistent_entities):
    """
    Specificity is defined as:
    log2(num_ancestors/num_all_nodes) / log2(1/num_all_nodes)
    'consistent_entities' is a list of consistent model entities. 
    :param str-list consistent_entities:
    :return float/None: return None if no object is consistent
    """
    specificity_score = []
    if consistent_entities:
      # k is the name of a consistent model entity
      for k in consistent_entities:
        entity_annotation = self.annotations.annotations[k]
        consistent_knowledge_resources = [ont \
                                         for ont in cn.KNOWLEDGE_TYPES_REP \
                                         if entity_annotation[ont]]
        entity_specificity = [ss.SPECIFICITY_FUNC[one_ont](entity_annotation[one_ont]) \
                              for one_ont in consistent_knowledge_resources]
        specificity_score.append(np.mean(entity_specificity))
      return np.mean(specificity_score)
    else:
      return None


def getMetrics(file, output="report"):
  """
  Using the AnnotationMetrics class,
  produces report on the three metrics.
  :param str file: address of model file (.xml)
  :param str output: output type ("report" or "table")
  :return str: or DataFrame?
  """
  metrics_class = AnnotationMetrics(model_file=file)
  if output=="report":
    res = ""
    res = res + "Model has total %d annotatable entities.\n" % \
                      len(metrics_class.annotations.annotations)
    res = res + "%d entities are annotated.\n" % len(metrics_class.annotated_entities)
    res = res + "%d entities are consistent.\n" % len(metrics_class.consistent_entities)
    res = res + "...\n"
    res = res + "Coverage is: {:.2f}\n".format(metrics_class.coverage) 
    res = res + "Consistency is: {:.2f}\n".format(metrics_class.consistency) 
    res = res + "Specificity is: {:.2f}\n".format(metrics_class.specificity) 
  elif output=="table":
    res_dict = {"num_annotatable_entities":[len(metrics_class.annotations.annotations)],
                "num_annotated_entities":[len(metrics_class.annotated_entities)],
                "num_consistent_entities":[len(metrics_class.consistent_entities)],
                "coverage":["{:.2f}".format(metrics_class.coverage)],
                "consistency":["{:.2f}".format(metrics_class.consistency)],
                "specificity":["{:.2f}".format(metrics_class.specificity)],
                }
    res = pd.DataFrame(res_dict)
  return res
















