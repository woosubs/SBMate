# specificity_score.py
"""
Methods to calculate
specificity score.
Return value is float.
Can be 0-1 or 0-100 scale
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
from SBMate import consistency_score as cs


def getOneSBOSpecificity(one_term):
  """
  Get specificity score for one SBO term
  :param str one_term:
  :return float:
  """
  # add 1 to include itself
  num_ancestors = len(nx.ancestors(cs.SBO_G, one_term))+1
  num_all_nodes = len(cs.SBO_G.nodes)
  spec_score = abs(np.round(np.log2(num_ancestors/num_all_nodes) / np.log2(1/num_all_nodes), 3))
  return spec_score

def getSBOSpecificity(inp_term):
  """
  Get specificity score of an SBO term.
  Terms is already assumed to be within 
  the correct ontology (i.e., consistent)
  :param str/str-list inp_term:
  :return float: between 0 and 1
  """
  if isinstance(inp_term, str):
    inp_list = [inp_term]
  else:
  	inp_list = inp_term
  return np.mean([getOneSBOSpecificity(val) for val in inp_list])

def getOneGOSpecificity(one_term):
  """
  Get specificity score for one GO term
  :param str one_term:
  :return float:
  """
  # Find appropriate GO root term
  root_term = cs.findGORoot(one_term)
  # add 1 to include itself
  num_ancestors = len(nx.ancestors(cs.GO_G, one_term))+1
  num_all_nodes = len(nx.ancestors(cs.GO_G, root_term))+1
  spec_score = abs(np.round(np.log2(num_ancestors/num_all_nodes) / np.log2(1/num_all_nodes), 3))
  return spec_score

def getGOSpecificity(inp_term):
  """
  Get specificity score of a GO term.
  Terms is already assumed to be within 
  the correct ontology (i.e., consistent)
  :param str/str-list inp_term:
  :return float: between 0 and 1
  """
  if isinstance(inp_term, str):
    inp_list = [inp_term]
  else:
  	inp_list = inp_term
  return np.mean([getOneGOSpecificity(val) for val in inp_list])

def getOneCHEBISpecificity(one_term):
  """
  Get specificity score for one CHEBI term
  :param str one_term:
  :return float:
  """
  # add 1 to include itself
  num_ancestors = len(nx.ancestors(cs.CHEBI_G, one_term))+1
  num_all_nodes = len(cs.CHEBI_G.nodes)
  spec_score = abs(np.round(np.log2(num_ancestors/num_all_nodes) / np.log2(1/num_all_nodes), 3))
  return spec_score

def getCHEBISpecificity(inp_term):
  """
  Get specificity score of a CHEBI term.
  Terms is already assumed to be within 
  the correct ontology (i.e., consistent)
  :param str/str-list inp_term:
  :return float: between 0 and 1
  """
  if isinstance(inp_term, str):
    inp_list = [inp_term]
  else:
  	inp_list = inp_term
  return np.mean([getOneCHEBISpecificity(val) for val in inp_list])

def getOthersSpecificity(inp_term):
  """
  Get specificity score of a term from
  other ontology systems, such as KEGG/UNIPROT
  Currently, default score is 1.0
  :param str/str-list inp_term:
  :return float: 
  """
  if isinstance(inp_term, str):
    inp_list = [inp_term]
  else:
  	inp_list = inp_term
  return 1.0

SPECIFICITY_FUNC = {'go':getGOSpecificity, 
                    'sbo': getSBOSpecificity,
                    'chebi': getCHEBISpecificity,
                    'kegg_species': getOthersSpecificity,
                    'kegg_process': getOthersSpecificity,
                    'uniprot': getOthersSpecificity}
