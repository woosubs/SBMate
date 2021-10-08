# metric_calculator.py
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
from SBMate import uniprot_kegg_analyzer as uka

# mapping reaction type to appropriate analyzer class
ANALYZER_DICT = {'go': da.DAGAnalyzer,
                 'sbo': da.DAGAnalyzer,
                 'chebi': da.DAGAnalyzer,
                 'kegg_species': uka.NonDAGAnalyzer,
                 'kegg_process': uka.NonDAGAnalyzer,
                 'uniprot': uka.NonDAGAnalyzer,
                }


class MetricCalculator(object):
  """
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

  def __init__(self, annotations, model_name):
    """
    Parameters
    ----------
    annotations: sbml_annotation.SortedSBMLAnnotation 
        Sorted annotations for the five knowledge resources.
    model: str
        Name of the model; will be index of the dataframe
    """
    self.annotations = annotations
    self.model_name = model_name

  def calculate(self):
    """
    Creates the metrics.

    Returns
    -------
    '': pd.DataFrame
        Merged dataframe for each calculated metric.
    """
    if self.annotations.annotations:
      len_annotatable_entities = len(self.annotations.annotations)
    else:
      len_annotatable_entities = 0.0
    annotated_entities, coverage = self._getCoverage()
    if annotated_entities:
      len_annotated_entities = len(annotated_entities)
    else:
      len_annotated_entities = None
    # calculate scores using the two types of Analyzer class
    consistent_entities, consistency = self._getConsistency(annotated_entities)
    if consistent_entities:
      len_consistent_entities = len(consistent_entities)
    else:
      len_consistent_entities = None
    specificity = self._getSpecificity(consistent_entities)
    entities_Df = self.mkDataframe({'annotatable_elements': len_annotatable_entities})
    coverage_Df = self.mkDataframe({'annotated_elements':len_annotated_entities,
                                    'coverage': coverage})
    consistency_Df = self.mkDataframe({'consistent_elements':len_consistent_entities,
                                       'consistency': consistency})
    specificity_Df = self.mkDataframe({'specificity': specificity})

    return pd.concat([entities_Df, coverage_Df, consistency_Df, specificity_Df], axis=1)

  def mkDataframe(self, score_info):
    """
    Creates a DataFrame using the entity information
    and the scores.

    Parameters
    ----------
    score_info: dict
        Dictionary of the score, number of entities, etc. 

    Returns
    -------
    '': pandas.DataFrame
        Dataframe including entities and the score. 
    """
    return pd.DataFrame(score_info, index=[self.model_name])


  def _getConsistency(self, annotated_entities):
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


  def _getSpecificity(self, consistent_entities):
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
      entities_specificity = [np.mean([one_analyzer.getSpecificity(one_analyzer.term_id) for \
                                       one_analyzer in consistent_entities[one_key]]) for \
                              one_key in consistent_entities.keys()]
      specificity_score = np.round(np.mean(entities_specificity), 2)
      return specificity_score
    else:
      return None

  def _getCoverage(self):
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
    list_annotated_entities = [k for \
                               k in \
                               self.annotations.annotations.keys() \
                               if any([self.annotations.annotations[k][ont] for ont \
                               in cn.KNOWLEDGE_TYPES_REP])]
    num_annotated_entities = len(list_annotated_entities)
    coverage_score = float(num_annotated_entities/num_annotatable_entities)
    return list_annotated_entities, np.round(coverage_score, 2)
