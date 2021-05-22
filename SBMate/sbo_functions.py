# sbo_functions.py

from urllib.request import urlopen
from bs4 import BeautifulSoup

START = "Name\n"
END = "Definition\n"
NO_VALUE = -1
NO_VALUE_SBO = "SBO:-000001"
NO_VALUE_SBO_RETURN = "No Term Provided"

def getOneSBOName(sbo_id):
  """
  Using the given SBO ID,
  parses and return its name.
  :param str sbo_id: e.g. "SBO:0000260"
  :return str: SBO name 
  """
  if sbo_id==NO_VALUE_SBO:
    return NO_VALUE_SBO_RETURN
  url = "https://www.ebi.ac.uk/sbo/main/" + sbo_id
  html = urlopen(url).read()
  soup = BeautifulSoup(html, features="html.parser")
  text = soup.get_text()
  sbo_name = text[(text.find(START)+len(START)):text.rfind(END)]
  return sbo_name

def getSBOString(sbo_num):
  """
  Returns a proper SBO term name 
  using the given SBO ID number (integer).
  :param int sbo_num: e.g. 260 
  :return str: SBO ID e.g. "SBO:0000260"
  """
  sbo_id = 'SBO:'+format(sbo_num, '07d')
  return sbo_id

