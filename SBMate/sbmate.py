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

from SBMate import dag_analyzer as da
from SBMate import uniprot_kegg_analyzer as uka

# mapping reaction type to the appropriate analyzer class
ANALYZER_DICT = {'go': da.DAGAnalyzer,
                 'sbo': da.DAGAnalyzer,
                 'chebi': da.DAGAnalyzer,
                 'kegg_species': uka.NonDAGAnalyzer,
                 'kegg_process': uka.NonDAGAnalyzer,
                 'uniprot': uka.NonDAGAnalyzer,
                }



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
    # self.consistent_entities, self.consistency = self.getConsistency(self.annotated_entities)
    # self.specificity = self.getSpecificity(self.consistent_entities)


    # a different take using two Analyzer classes
    self.consistent_entities, self.consistency = self.getConsistency(self.annotated_entities)
    self.specificity = self.getSpecificity(self.consistent_entities)

  def getConsistency(self, annotated_entities):
    """
    Calculate consistency using analylzer classes. 
    Consistency is defined as:
    (# consistently annotated entities) / (# annotated entities)
    'annotated_entities' is a list of annotated model entity names.
    Returns dictionary of entity & analyzer instances,
    as well as consistency score.
    :param str-list annotated_entities:
    :return dict(Analyzer-list)/None: return None if no object is annotated
    :return float/None: return None if no object is annotated
    """
    if not annotated_entities:
      return None, None
    consistent_entities = []
    consistent_dicts = dict()
    for anot_key in annotated_entities:
      one_anot = self.annotations.annotations[anot_key]
      # annotated entities
      one_entity_onts = [ANALYZER_DICT[key](term_id=one_anot[key],
                                            ontology=key,
                                            object_type=one_anot['object_type']) \
                         for key in ANALYZER_DICT if one_anot[key]]

      # if consistent for all ontologies, update list of consistent objects
      if all([r.consistent for r in one_entity_onts]):
        consistent_dicts[anot_key] = one_entity_onts
    consistency_score = np.round(len(consistent_dicts.keys())/len(annotated_entities), 2)
    return consistent_dicts, consistency_score


  def getSpecificity(self, consistent_entities):
    """
    Calculate specificity using analyzer classes.
    Specificity is defined as:
    log(num_ancestors/num_all_nodes) / log(1/num_all_nodes)
    'consistent_entities' is a list of consistent model entities. 
    :param dict(Analyzer-list) consistent_entities:
    :return float/None: return None if no object is consistent
    """
    # calculates specificity only if it has at least one consistent entity
    if consistent_entities:
      # Below is the longer (and slower) version of lines 103-105
      # specificity = []
      # for one_key in consistent_entities.keys():
      #   one_score = [one_analyzer.getSpecificity(one_analyzer.term_id) for one_analyzer in consistent_entities[one_key]]
      #   specificity.append(np.mean(one_score))
      # specificity_score = np.mean(specificity)
      entities_specificity = [np.mean([one_analyzer.getSpecificity(one_analyzer.term_id) for \
                                       one_analyzer in consistent_entities[one_key]]) for \
                              one_key in consistent_entities.keys()]
      specificity_score = np.round(np.mean(entities_specificity), 2)
      return specificity_score
    else:
      return None


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

  # Below are old version
  # def getConsistency(self, annotated_entities):
  #   """
  #   Consistency is defined as:
  #   (# consistently annotated entities) / (# annotated entities)
  #   'annotated_entities' is a list of annotated model entities.
  #   :param str-list annotated_entities:
  #   :return str-list/None: return None if no object is annotated
  #   :return float/None: return None if no object is annotated
  #   """
  #   if annotated_entities:
  #     consistent_entities = []
  #     # k is the name of each model entity
  #     for k in annotated_entities:
  #       entity_annotation = self.annotations.annotations[k]
  #       entity_type = entity_annotation['object_type']
  #       annotated_knowledge_resources = [ont \
  #                                        for ont in cn.KNOWLEDGE_TYPES_REP \
  #                                        if entity_annotation[ont]]
  #       # By setup, annotated_knowledge_resources should have at least one item
  #       is_consistent_list = [cs.CONSISTENCY_FUNC[one_ont](entity_annotation[one_ont], entity_type) \
  #                             for one_ont in annotated_knowledge_resources]
  #       if all(is_consistent_list):
  #         consistent_entities.append(k) 
  #     # if there is at least one annotated entity, return intended values
  #     return consistent_entities, float(len(consistent_entities) / len(annotated_entities))
  #   # else happens if no object is annotated
  #   else: 
  #     return None, None

  # def getSpecificity(self, consistent_entities):
  #   """
  #   Specificity is defined as:
  #   log2(num_ancestors/num_all_nodes) / log2(1/num_all_nodes)
  #   'consistent_entities' is a list of consistent model entities. 
  #   :param str-list consistent_entities:
  #   :return float/None: return None if no object is consistent
  #   """
  #   specificity_score = []
  #   if consistent_entities:
  #     # k is the name of a consistent model entity
  #     for k in consistent_entities:
  #       entity_annotation = self.annotations.annotations[k]
  #       consistent_knowledge_resources = [ont \
  #                                        for ont in cn.KNOWLEDGE_TYPES_REP \
  #                                        if entity_annotation[ont]]
  #       entity_specificity = [ss.SPECIFICITY_FUNC[one_ont](entity_annotation[one_ont]) \
  #                             for one_ont in consistent_knowledge_resources]
  #       specificity_score.append(np.mean(entity_specificity))
  #     return np.mean(specificity_score)
  #   else:
  #     return None


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
















