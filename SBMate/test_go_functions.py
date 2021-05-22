# test_go_functions.py
"""
Tests go_functions.py
# testing
python -m unittest test_go_functions
"""

import os
import unittest
import go_functions as gf 

one_without_go = 'abcdefg'

one_with_one_go = '<annotation>\n  ' +\
  '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" ' +\
  'xmlns:bqmodel="http://biomodels.net/model-qualifiers/" xmlns:bqbiol="http://biomodels.net/biology-qualifiers/">\n    ' +\
  '<rdf:Description rdf:about="#_905823">\n      <bqbiol:isVersionOf>\n        <rdf:Bag>\n          ' +\
  '<rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0006402"/>\n        </rdf:Bag>\n      ' +\
  '</bqbiol:isVersionOf>\n    </rdf:Description>\n  </rdf:RDF>\n</annotation>'

one_with_two_gos = '<annotation>\n  <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"  ' + \
  'xmlns:bqmodel="http://biomodels.net/model-qualifiers/" xmlns:bqbiol="http://biomodels.net/biology-qualifiers/">\n    ' + \
  '<rdf:Description rdf:about="#metaid_0000106">\n      <bqbiol:isVersionOf>\n        <rdf:Bag>\n          ' + \
  '<rdf:li rdf:resource="http://identifiers.org/go/GO:0005515"/>\n   <rdf:li rdf:resource="http://identifiers.org/go/GO:0005102"/>\n  ' + \
  '</rdf:Bag>\n      </bqbiol:isVersionOf>\n    </rdf:Description>\n  </rdf:RDF>\n</annotation>'

class TestMolecule(unittest.TestCase):

  def testParseGO(self):
    self.assertEqual(gf.parseGO(one_without_go), [])
    self.assertEqual(gf.parseGO(one_with_one_go), ["GO:0006402"])
    self.assertEqual(set(gf.parseGO(one_with_two_gos)), {"GO:0005515", "GO:0005102"})

  def testGetGONum(self):
    self.assertEqual(gf.getGONum("GO:0033192"), "0033192")
    self.assertEqual(gf.getGONum("ABC"), None)
    self.assertEqual(gf.getGONum("SBO:0033192"), None)

  def testGetGORelationsToTop(self):
  	result = gf.getGORelationsToTop(input_go="GO:0008152")
  	result_f = gf.getGORelationsToTop(input_go="GO:0000060")
  	self.assertEqual(result['numberOfHits'], 1)
  	self.assertEqual(len(result['results']), 1)
  	self.assertEqual(result['results'][0][0]['child'], "GO:0008152")
  	self.assertEqual(result['results'][0][0]['relationship'], "is_a")
  	self.assertFalse(result_f)

  def testGetGOAspect(self):
    self.assertEqual(gf.getGOAspect("GO:0019538"), "biological_process")
    self.assertEqual(gf.getGOAspect("GO:0016772"), "molecular_function")
    self.assertEqual(gf.getGOAspect("GO:0043226"), "cellular_component")




