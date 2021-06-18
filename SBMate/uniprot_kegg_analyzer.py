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


ONT_TO_URL= {"uniprot":"https://www.uniprot.org/uniprot/",
             "kegg_process":"https://www.genome.jp/entry/",
             "kegg_species":"https://www.genome.jp/entry/",
            }
KEGG_ERROR_MESSAGE = "No such data was found"


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
    self.consistent = self.getConsistency(inp_term=self.term_id)


  def getOneTermConsistency(self, one_term):
    """
    Get consistency of one term,
    by connecting to the url.
    :param str one_term:
    :return bool:
    """
    r = requests.get(ONT_TO_URL[self.ontology]+one_term)
    # for kegg, needs to check whether the text is in the page
    if KEGG_ERROR_MESSAGE in r.text:
      return False
    else:
      return r.ok

  def getConsistency(self, inp_term):
    """
    Using getOneTermConsistency(),
    check if the terms are consistent.
    :param str/list inp_term:
    :return bool:
    """
    # first, check if the input term is in correct format
    if isinstance(inp_term, str):
      inp_list = [inp_term]
    elif isinstance(inp_term, list):
      # if it is a list, check whether all terms are string
      if sum([isinstance(t, str) for t in inp_term])==len(inp_term):
        inp_list = inp_term
      else:
        return False
    else:
      return False
    # second, check if the object type and ontology match
    if not self.ontology in cn.OBJECT_ONT_MAP_FILT[self.object_type]:
      return False
    # finally, query the term and get consistency
    res = [self.getOneTermConsistency(t) for t in inp_list]
    if all(res):
      return True
    else:
      return False

  def getSpecificity(self, inp_term):
    """
    Get specificity score of one or more terms.
    Specificity is 1 for uniprot and KEGG, 
    as long as the therms are consistent.
    :param str/str-list inp_term:
    :return float: if consistent, assign 1.0
    """
    if not self.consistent:
      return None
    else:
      return float(1.0)















