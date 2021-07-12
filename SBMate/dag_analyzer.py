# dag_analyzer.py
"""
Analyzer class for ontology terms.
This class is for DAG-type knowledge resources, 
i.e.,  GO, SBO, and CHEBI.
The two classes calculate consistency & specificity, 
and returns appropriate values. 
"""

import collections
import libsbml
import networkx as nx
import numpy as np
import os
import pickle5 as pickle
from SBMate import constants as cn

# Load ontology graphs
SBO_G = pickle.load(open(os.path.join(cn.RESOURCE_DIR, "sbo_graph.gpickle"), 'rb'))
CHEBI_G = pickle.load(open(os.path.join(cn.RESOURCE_DIR, "chebi_graph.gpickle"), 'rb'))
GO_G = pickle.load(open(os.path.join(cn.RESOURCE_DIR, "go_graph.gpickle"), 'rb'))

# Mapping ontology into specific graph
ONT_TO_G = dict({"go":GO_G, "sbo":SBO_G, "chebi":CHEBI_G})
# Mapping ontology to list of roots
ONT_TO_ROOT = dict({"go": cn.GO_ROOTS, "sbo":cn.SBO_ROOTS, "chebi":cn.CHEBI_ROOTS})


class DAGAnalyzer(object):
  """
  Analyzer for GO, SBO, and CHEBI.
  Calculates object-level consistency 
  and specificity. 
  Terms are hierarchically arranged,
  having one or a few terms as roots for
  the rest of the terms. 

  Attributes
  ----------
  term_id: str-list
      List of identifiers to analyze.
  ontology: str
      Appropriate ontology type.
  object_type: libsbml.AutoProperty
      Type of the model entity.
  dag: networkx.DiGraph
      Directed Acyclic Graph for ontology system.
  possible_roots: str-list
      List of identifiers (roots) for all terms 
      within the system.
  term_to_root: None -> dict
      Dictionary, mapping each identifier: its root.
  consistent: bool
      Bool determining whether the entity-object is consistent.   

  Methods
  -------
  findRoot(inp_term)
      Find an appropriate root of one identifier.
  getConsistency (inp_term)
      Check if the given term (ontology identifier)
      is consistent.
  getOneTermSpecificity (one_term)
      Get the specificity of one identifier.
  getSpecificity (inp_term)
      Calculate specificity of a list of terms,
      using getOneTermSpecificity method.
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
        Type of model entity. For example, libsbml.Reaction
    """
    self.term_id = term_id
    self.ontology = ontology
    self.object_type = object_type
    self.dag = ONT_TO_G[self.ontology]
    self.possible_roots = ONT_TO_ROOT[self.ontology]
    self.term_to_root = None
    self.consistent = self.getConsistency(inp_term=self.term_id)

  def findRoot(self, inp_term):
    """
    Find the appropriate root for
    the given term, 
    as specified by ONT_TO_ROOT.
    If none is found, return None.
    (which is an error)

    Parameters
    ----------
    inp_term: str
        Identifier (string) to check. 

    Returns
    -------
    one_ances: str, or None
        Identifier of the root for the inp_term. 
    """
    if inp_term in self.dag:
      for one_ances in self.possible_roots:
        has_p = nx.has_path(self.dag, source=inp_term, target=one_ances)
        if has_p:
          return one_ances
    return None

  def getConsistency(self, inp_term):
    """
    Tests if the given term
    or the list of the terms
    are consistent.
    inp_term should be either string or
    a list of strings
    (checked at the beginning).

    Parameters
    ----------
    inp_term: str/str-list
        Identifier (or list of identifiers)

    Returns
    -------
    '': bool
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
    # if the term(s) are in correct format, check parents (roots)
    par_dict = {one_term:self.findRoot(one_term) for one_term in inp_list}
    pars = [par_dict[k] for k in par_dict.keys()]
    par_types = set([cn.DAG_ROOT_MAP[self.ontology][ele] for ele in pars])
    acceptable_par_types = cn.OBJECT_ONT_MAP_FILT[self.object_type]
    if par_types <= acceptable_par_types:
      self.term_to_root = par_dict
      return True
    else:
      return False

  def getOneTermSpecificity(self, one_term):
    """
    Get specificity score for one term.

    Parameters
    ----------
    one_term: str
         Identifier to check specificity.

    Returns
    -------
    spec_score: float
        Specificity score. 
    """
    if not self.consistent or one_term not in self.dag:
      return None
    # Find appropriate root term
    root_term = self.term_to_root[one_term]
    # add 1 to include itself
    num_ancestors = len(nx.ancestors(self.dag, one_term))+1
    num_all_nodes = len(nx.ancestors(self.dag, root_term))+1
    spec_score = abs(np.log(num_ancestors/num_all_nodes) / np.log(1/num_all_nodes))
    return spec_score

  def getSpecificity(self, inp_term):
    """
    Get specificity score of one or more terms,
    using getOneTermSpecificity().
    Specificity is calculated only if
    the term is already consistent.

    Parameters
    ----------
    inp_term: str/str-list
        Identifier(s) to check specificity.

    Returns
    -------
    '': float / None
        Specificity score (averaged within the same ontology).
    """
    if not self.consistent:
      return None
    if isinstance(inp_term, str):
      inp_list = [inp_term]
    else:
      inp_list = inp_term
    if set(inp_list) <= self.term_to_root.keys():
      res = [self.getOneTermSpecificity(val) for val in inp_list]
      return np.mean(res)
    else:
      print("Calculate consistency first!")
      return None


