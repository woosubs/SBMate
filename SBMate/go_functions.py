# go_functions.py
"""
Parse GO annotations
and get information
"""

import re, requests, sys

GO_PREFIX = "GO"
GO_BIO_PROC = "GO:0008150"
GO_MOL_FUNC = "GO:0003674"
GO_CELL_COMP = "GO:0005575"
# annotation terms defined within
# 'annotatable' objects, such as
# model, species, reaction, compartments (and possibly parameters)
GOS = {'go', 'GO', 'obo.go'}


def parseGO(go_str):
  """
  Parse string to extract
  'all' GO terms, in a format
  GO:XXXXXXX
  :param str go_str: 
  :return str-list
  """
  # all indices of 'GO' instances
  go_locs = [g.start() for g in re.finditer(GO_PREFIX, go_str)]
  # if no GO term exists, return an empty list
  if len(go_locs) == 0:
    return []
  go_ranges = [go_str[go_loc:go_loc+12] for go_loc in go_locs]
  go_specs = [re.findall(r'\d+', go_range) for go_range in go_ranges]
  # str->int->formatted str needed,
  # as some GO terms do not have proper digits
  go_vals = [int(go_spec[-1]) for go_spec in go_specs if len(go_spec)>0]
  # return only unique terms (some reactions have identical GO terms)
  go_res = list(set([GO_PREFIX + ":" + "{:07d}".format(go_val) for go_val in go_vals]))
  return go_res


def getGONum(go_str):
  """
  Parse the number part from a
  GO term, in a format
  GO:XXXXXXX
  :param str go_str: 
  :return None/str
  """
  if 'GO' not in go_str:
    return None
  go_parts = go_str.split(":")
  if len(go_parts)>1:
  	return go_parts[1]
  # Return None if the format doesn't fit
  else:
    return None


def getGORelationsToTop(input_go, par_go=GO_BIO_PROC):
  """
  Connect to API and get relationships
  between input_go and par_go
  :param str input_go:
  :return False/dict
  """
  url_base = "https://www.ebi.ac.uk/QuickGO/services/ontology/go/terms/"
  go_spec = "GO%3A" + getGONum(input_go) + "/paths/GO%3A" + getGONum(par_go) + "?relations=is_a%2Cpart_of"
  requestURL = url_base + go_spec
  r = requests.get(requestURL, headers={"Accept" : "application/json"})
  if r.ok:
  	res = r.json()
  else:
  	res = False
  return res


def getGOAspect(input_go):
  """
  Determine the GO type,
  i.e., one of 
  1) Molecular Function
  2) Biological Process
  3) Cellular Components
  :param str input_go:
  :return str/None:
  """
  url = "https://www.ebi.ac.uk/QuickGO/services/ontology/go/terms/"
  try:
    url = url + "GO%3A" + getGONum(input_go) + "/ancestors?relations=is_a"
    r = requests.get(url, headers={"Accept" : "application/json"})
    result = r.json()
    return result['results'][0]['aspect'] 
  except:
    return None



