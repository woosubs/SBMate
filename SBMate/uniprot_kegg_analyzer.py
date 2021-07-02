# uniprot_kegg_analyzer.py
"""
Analyzer class for non-DAG knowledge resources
such as UNIPROT and KEGG.
The two classes calculate consistency & specificity, 
and returns appropriate values. 
"""

import collections
import libsbml
import numpy as np
import os
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

  Attributes
  ----------
  term_id: str-list
      List of identifiers to analyze.
  ontology: str
      Appropriate ontology type.
  object_type: libsbml.AutoProperty
      Type of the model entity.
  consistent: bool
      Bool determining whether the entity-object is consistent.     

  Methods
  -------
  getOneTermConsistency (one_term)
      Check if the given term (ontology identifier)
      is consistent, using url. 
  getConsistency (inp_term)
      Check if the given term (ontology identifier)
      is consistent.      
  getSpecificity (inp_term)
      Get specificity of a list of terms.
      These ontologies are 1.0 if consistent. 
  """

  def __init__(self, term_id, ontology,
               object_type):
    """
    Parameters
    ----------
    term_id: str-list
        Identifier to analyze
    ontology: str
        Ontology (knowledge resource).
        Should be one of {'go', 'sbo', 'chebi'}.
    object_type: libsbml.AutoProperty
        Type of model entity. For example, libsbml.Reactionß
    """
    self.term_id = term_id
    self.ontology = ontology
    self.object_type = object_type
    self.consistent = self.getConsistency(inp_term=self.term_id)


  def getOneTermConsistency(self, one_term):
    """
    Get consistency of one term,
    by connecting to the url
    and checking it works. 

    Parameters
    ----------
    one_term: str
        One identifier string to check.

    Returns
    -------
    '': bool
        True if consistent; otherwise False
    """
    r = requests.get(ONT_TO_URL[self.ontology]+one_term)
    # for kegg, needs to check whether the text below is in the page
    if KEGG_ERROR_MESSAGE in r.text:
      return False
    else:
      return r.ok

  def getConsistency(self, inp_term):
    """
    Using getOneTermConsistency(),
    check if the terms are consistent.

    Parameters
    ----------
    inp_term: str/str-list
        A list of terms,
        in the same ontology,
        from a single model entity. 

    Returns
    -------
    '': bool
        True if all terms are consistent; otherwise False.
    """
    # First, check if the input term is in correct format
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

    Parameters
    ----------
    inp_term: str/str-list
        List of identifiers to check specificity

    Returns
    -------
    '': float/None
        If consistent, 1.0; otherwise None.
    """
    if not self.consistent:
      return None
    else:
      return float(1.0)


