# uniprot_kegg_analyzer.py
"""
Analyzer class for non-DAG knowledge resources
such as UNIPROT and KEGG.
The two classes calculate consistency & specificity, 
and returns appropriate values. 
"""

import collections
import libsbml
import networkx as nx
import numpy as np
import os
import pickle
import re
import requests
from SBMate import constants as cn


class NonDAGAnalyzer(object):
  """
  Analyzer for UNIPROT and KEGG.
  """

  def __init__(self, term_id, ontology,
               object_type):
    """
    param: str/list term_id: identifier to analyze
    param: str ontology: one of "uniprot", "kegg_process", and "kegg_species"
    param: libsbml.AutoProperty object_type: 
           one of model entity types, e.g., libsbml.Species
    """
    self.term_id = term_id
    self.ontology = ontology
    self.object_type = object_type
    