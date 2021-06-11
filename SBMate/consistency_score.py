# consistency_score.py
"""
Methods to calculate
consistency score.
Main return value is bool. 
(consistent vs. not consistent)
"""

import collections
import libsbml
import networkx as nx
import os
import pickle
import re
import requests
from SBMate import constants as cn

# Load ontology graphs
SBO_G = nx.read_gpickle(os.path.join(cn.RESOURCE_DIR, "sbo_graph.gpickle"))
CHEBI_G = nx.read_gpickle(os.path.join(cn.RESOURCE_DIR, "chebi_graph.gpickle"))
GO_G = nx.read_gpickle(os.path.join(cn.RESOURCE_DIR, "go_graph.gpickle"))


def findGORoot(inp_go_term):
  """
  Find the appropriate root for
  the given go term. 
  Three possibilities -
  a. Biological Process
  b. Molecular Function
  c. Cellular Component
  If none is found, return None
  (which is an error)
  :param str inp_go_term:
  :return str/None
  """
  if inp_go_term in GO_G:
    for one_ances in cn.GO_ROOTS:
      has_p = nx.has_path(GO_G, source=inp_go_term, target=one_ances)
      if has_p:
        return one_ances
  return None

def findSBORoot(inp_sbo_term):
  """
  find the parent of the given sbo term
  from the list. 
  :param str inp_sbo_term:
  :return str/None
  """
  if inp_sbo_term in SBO_G:
    for one_ances in cn.SBO_ROOTS:
      has_p = nx.has_path(SBO_G, source=inp_sbo_term, target=one_ances)
      if has_p:
        return one_ances
  return None

def isGOConsistent(inp_go, inp_type):
  """
  test if the GO term
  or the list of GO terms
  are consistent
  :param str/list-str inp_go:
  :param libsbml.AutoProperty inp_type:
  :return bool:
  """
  go_ancestor_map = {cn.GO_BIO_PROC: cn.BIOL_PROC,
                     cn.GO_MOL_FUNC: cn.MOLE_FUNC,
                     cn.GO_CELL_COMP: cn.CELL_COMP,
                     None: "None"
                    }
  if isinstance(inp_go, str):
    inp_list = [inp_go]
  elif isinstance(inp_go, list):
    inp_list = inp_go
  else:
    return False
  go_pars = [findGORoot(go_term) for go_term in inp_list]
  go_type = set(["go:"+go_ancestor_map[ele] for ele in go_pars])
  go_valid_type = cn.OBJECT_ONT_MAP_FILT[inp_type]
  if go_type <= go_valid_type:
    return True
  else:
    return False

def isSBOConsistent(inp_sbo, inp_type):
  """
  test if the SBO term
  or the list of SBO terms
  are consistent
  :param str/list-str inp_sbo:
  :param libsbml.AutoProperty inp_type:
  :return bool:
  """
  sbo_ancestor_map = cn.SBO_ROOT_DICT
  sbo_ancestor_map[None] = "None"
  if isinstance(inp_sbo, str):
    inp_list = [inp_sbo]
  elif isinstance(inp_sbo, list):
    inp_list = inp_sbo
  else:
    return False
  sbo_pars = [findSBORoot(sbo_term) for sbo_term in inp_list]
  sbo_type = set([sbo_ancestor_map[ele] for ele in sbo_pars])
  sbo_valid_type = cn.OBJECT_ONT_MAP_FILT[inp_type]
  if sbo_type <= sbo_valid_type:
    return True
  else:
    return False

def isCHEBIConsistent(inp_chebi, inp_type):
  """
  test if the CHEBI term
  or the list of SBO terms
  are consistent
  :param str/list-str inp_chebi:
  :param libsbml.AutoProperty inp_type:
  :return bool:
  """
  # simply check if the term is connected with
  # the chemical entity: CHEBI:24431
  def hasCHEBIParent(inp_che):
    if inp_che not in CHEBI_G:
      return False
    else:
      return nx.has_path(CHEBI_G, source=inp_che, target='CHEBI:24431')
  # check inp_chebi
  if isinstance(inp_chebi, str):
    inp_list = [inp_chebi]
  elif isinstance(inp_chebi, list):
    inp_list = inp_chebi
  else:
    return False
  # check inp_type
  if inp_type not in [cn.SPECIES, cn.COMPARTMENT]:
    return False
  # Now, check the link
  is_chebi = [hasCHEBIParent(ele) for ele in inp_list]
  if sum(is_chebi)==len(is_chebi):
    return True
  else:
    return False

def isUNIPROTConsistent(inp_uniprot, inp_type):
  """
  Briefly check if object type is libsbml.Species
  and if the identifier exists by
  connecting to the webpage.
  Returns only if r.ok is False for an identifier
  or if the type is not cn.SPECIES. 
  :param str/list-str inp_chebi:
  :param libsbml.AutoProperty inp_type:
  :return bool:
  """
  if isinstance(inp_uniprot, str):
    inp_list = [inp_uniprot]
  elif isinstance(inp_uniprot, list):
    inp_list = inp_uniprot
  else:
    return False
  if inp_type in [cn.SPECIES]:
    try:
      request_res = []
      for one_uniprot in inp_list:
        r = requests.get('https://www.uniprot.org/uniprot/' + one_uniprot)
        request_res.append(r.ok)
      if False in request_res:
        return False
      else:
        return True
    except:
      return True
  else:
    return False

def isKEGGSpeciesConsistent(inp_kegg_species, inp_type):
  """
  Briefly check if object type is cn.SPECIES.
  Then, checks if KEGG url can be accessed 
  without generating 'No such data was found.'
  :param str/list-str inp_chebi:
  :param libsbml.AutoProperty inp_type:
  :return bool:
  """
  if isinstance(inp_kegg_species, str):
    inp_list = [inp_kegg_species]
  elif isinstance(inp_kegg_species, list):
    inp_list = inp_kegg_species
  if inp_type in [cn.SPECIES]:
    request_res = []
    for one_kegg in inp_list:
      r = requests.get('https://www.genome.jp/entry/' + one_kegg)
      if 'No such data was found' in r.text:
        request_res.append(False)
      else:
        request_res.append(True)
    if False in request_res:
      return False
    else:
      return True
  else:
    return False

def isKEGGProcessConsistent(inp_kegg_process, inp_type):
  """
  Briefly check if object type is appropriate,
  meaning bqbiol:is(VersionOf) Reaction or Model.
  Then, checks if KEGG url can be accessed 
  without generating 'No such data was found.'
  :param str/list-str inp_chebi:
  :param libsbml.AutoProperty inp_type:
  :return bool:
  """
  if isinstance(inp_kegg_process, str):
    inp_list = [inp_kegg_process]
  elif isinstance(inp_kegg_process, list):
    inp_list = inp_kegg_process
  if inp_type in [cn.MODEL, cn.REACTION]:
    request_res = []
    for one_kegg in inp_list:
      r = requests.get('https://www.genome.jp/entry/' + one_kegg)
      if 'No such data was found' in r.text:
        request_res.append(False)
      else:
        request_res.append(True)
    if False in request_res:
      return False
    else:
      return True
  else:
    return False


CONSISTENCY_FUNC = {'go':isGOConsistent, 
                    'sbo': isSBOConsistent,
                    'chebi': isCHEBIConsistent,
                    'kegg_species': isKEGGSpeciesConsistent,
                    'kegg_process': isKEGGProcessConsistent,
                    'uniprot': isUNIPROTConsistent}

