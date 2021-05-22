# annotation_functions.py
"""
Methods needed to pull out annotations
from libsbml files, especially biomodels.
"""

import re, requests, sys


# new version for multiple chunk occurrence
def getOntAnnotation(input_annotation):
  """
  Parse string and return string annotation,
  marked with <bqbiol:is> or <bqbiol:isVersionOf>.
  If neither exists, return an empty string ''
  :param str input_annotation:
  :return str:
  """
  is_str = ''
  isVersionOf_str = ''
  is_str_match = re.findall('<bqbiol:is>.*?<\/bqbiol:is>',
                           input_annotation,
                           flags=re.DOTALL)
  if len(is_str_match)>0:
    is_str_match_filt = [s.replace("      ", "") for s in is_str_match]
    is_str = '\n'.join(is_str_match_filt)

  is_VersionOf_str_match = re.findall('<bqbiol:isVersionOf>.*?<\/bqbiol:isVersionOf>',
                                     input_annotation,
                                     flags=re.DOTALL)
  if len(is_VersionOf_str_match)>0:
    is_VersionOf_str_match_filt = [s.replace("      ", "") for s in is_VersionOf_str_match]
    isVersionOf_str = '\n'.join(is_VersionOf_str_match_filt)
  #
  combined_str = is_str + isVersionOf_str
  return combined_str

