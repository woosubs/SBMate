# sbmate.py
# calculate annotation scores

import libsbml
import networkx as nx
import numpy as np
import os
import pandas as pd
import re
import requests
from SBMate import constants as cn
from SBMate import dag_analyzer as da
from SBMate import sbml_annotation as sa
from SBMate import uniprot_kegg_analyzer as uka

# mapping reaction type to appropriate analyzer class
ANALYZER_DICT = {'go': da.DAGAnalyzer,
                 'sbo': da.DAGAnalyzer,
                 'chebi': da.DAGAnalyzer,
                 'kegg_species': uka.NonDAGAnalyzer,
                 'kegg_process': uka.NonDAGAnalyzer,
                 'uniprot': uka.NonDAGAnalyzer,
                }


class AnnotationMetrics(object):
  """
  Collects model annotations and
  calculates three scores:
  1. coverage
  2. consistency
  3. specificity

  Attributes
  ----------
  annotations: sbml_annotation.SortedSBMLAnnotation 
      Sorted annotations for each knowledge resource.
  annotated_entities: str-list
      List of model entity names that are annotated.
  consistent_entities: dict
      Dictionary of model entity name: list of consistent analyzer classes.
  coverage: float
      Model coverage score.
  consistency: float
      Model consistency score. 
  specificity: float
      Model specificity score. 

  Methods
  -------
  getCoverage(annotated_entities)
      Calculates model coverage score.
  getConsistency
      Calculates model consistency score.
  getSpecificity
      Calculates model specificity score. 
  """
  def __init__(self, model_file):
    """
    Parameters
    ----------
    model_file: str 
        Address/name of the .xml model file
    """
    self.annotations = sa.SortedSBMLAnnotation(file=model_file)
    self.annotated_entities, self.coverage = self.getCoverage()
    # calculate scores using the two types of Analyzer class
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

    Parameters
    ----------
    annotated_entities: str-list 
        List of annotated entities.

    Returns
    -------
    consistent_dicts: dict (str: Analyzer-list) / None
        Dictionary of consistenty entities and list of analyzers.
    consistency_score: float/None
        Consistency score. None if no object is annotated.
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

    Parameters
    ----------
    consistent_entities: dict (str: Analyzer-list)
         Dictionary of consistenty entities and list of analyzers.

    Returns
    -------
    specificity_score: float
        Model specificity score.
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

    Returns
    -------
    list_annotated_entities: str-list
        List of annotated model entity names.
    '': float
        Coverage score. 
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



def getMetricsReport(metrics_tuple):
  """
  Create a string report for
  an AnnotationMetrics class.

  Parameters
  ----------
  metrics_tuple: tuple (str, AnnotationMetrics)
      A tuple of file name and an AnnotationMetrics class instance

  Returns
  -------
  report: str
      Report summarizing the metrics
  """
  model_name = metrics_tuple[0]
  metrics_class = metrics_tuple[1]
  report = ""
  report = report + "Model \'%s\' has total %d annotatable entities.\n" % \
                     (model_name, len(metrics_class.annotations.annotations))
  report = report + "%d entities are annotated.\n" % len(metrics_class.annotated_entities)
  report = report + "%d entities are consistent.\n" % len(metrics_class.consistent_entities)
  report = report + "...\n"
  report = report + "Coverage is: {:.2f}\n".format(metrics_class.coverage) 
  report = report + "Consistency is: {:.2f}\n".format(metrics_class.consistency) 
  report = report + "Specificity is: {:.2f}\n".format(metrics_class.specificity)
  return report


def getMetricsTable(metrics_tuple):
  """
  Create a table (data frame) for
  an AnnotationMetrics class.

  Parameters
  ----------
  metrics_tuple: tuple (str, AnnotationMetrics)
      A tuple of file name and an AnnotationMetrics class instance

  Returns
  -------
  table: pandas.DataFrame
      DataFrame summarizing metrics
  """
  model_name = metrics_tuple[0]
  metrics_class = metrics_tuple[1]
  res_dict = {model_name: {"num_annotatable_entities":len(metrics_class.annotations.annotations),
                           "num_annotated_entities":len(metrics_class.annotated_entities),
                           "num_consistent_entities":len(metrics_class.consistent_entities),
                           "coverage":"{:.2f}".format(metrics_class.coverage),
                           "consistency":"{:.2f}".format(metrics_class.consistency),
                           "specificity":"{:.2f}".format(metrics_class.specificity),
                          }
             }
  table = pd.DataFrame.from_dict(res_dict, orient='index')
  return table


def getMetrics(file, output="report"):
  """
  Using the AnnotationMetrics class,
  produces report on the three metrics.

  Parameters
  ----------
  file: str/str-list
      Address(es) of model file (.xml).
      Should be string or list of string.
  output: str
      The type of output ("report" or "table").

  Returns
  --------
  res: str / pandas.DataFrame / None
      Final report (summary) of the model. 
      Return None if input type is incorrect. 
  """

  if isinstance(file, str):
    file_list = [file]
  elif isinstance(file, list):
    if all([isinstance(one_file, str) for one_file in file]):
      file_list = file
    else:
      return None
  else:
    return None

  metrics_tuple_list = [(one_file[-19:], AnnotationMetrics(model_file=one_file)) for one_file in file_list]
  if output=="report":
    res_list = [getMetricsReport(one_tuple) for one_tuple in metrics_tuple_list]
    res = ('\n').join(res_list)
  elif output=="table":
    res_list = [getMetricsTable(one_tuple) for one_tuple in metrics_tuple_list]
    res = pd.concat(res_list)
  return res







