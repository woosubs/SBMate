# test_annotation_functions.py
"""
Tests annotation_functions.py
# testing
python -m unittest test_annotation_functions
"""

import os
import unittest
import annotation_functions as af 

# annottions are originally from BIOMODEL 12
annotation_isVersionOf = '<annotation>\n  ' + \
  '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" ' + \
  'xmlns:bqmodel="http://biomodels.net/model-qualifiers/" xmlns:bqbiol="http://biomodels.net/biology-qualifiers/">\n    ' + \
  '<rdf:Description rdf:about="#_905769">\n      ' + \
  '<bqbiol:isVersionOf>\n        <rdf:Bag>\n          ' + \
  '<rdf:li rdf:resource="http://identifiers.org/chebi/CHEBI:33699"/>\n          ' + \
  '<rdf:li rdf:resource="http://identifiers.org/kegg.compound/C00046"/>\n        </rdf:Bag>\n      ' + \
  '</bqbiol:isVersionOf>' + \
  '\n      <bqbiol:encodes>\n        <rdf:Bag>\n          ' + \
  '<rdf:li rdf:resource="http://identifiers.org/uniprot/P03023"/>\n        </rdf:Bag>\n      ' + \
  '</bqbiol:encodes>\n    </rdf:Description>\n  </rdf:RDF>\n</annotation>'
result_isVersionOf = '<bqbiol:isVersionOf>\n        <rdf:Bag>\n          ' + \
  '<rdf:li rdf:resource="http://identifiers.org/chebi/CHEBI:33699"/>\n          ' + \
  '<rdf:li rdf:resource="http://identifiers.org/kegg.compound/C00046"/>\n        </rdf:Bag>\n      ' + \
  '</bqbiol:isVersionOf>'
result_isVersionOf = result_isVersionOf.replace("      ", "")


annotation_is = '<annotation>\n  ' + \
  '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" ' + \
  'xmlns:bqmodel="http://biomodels.net/model-qualifiers/" xmlns:bqbiol="http://biomodels.net/biology-qualifiers/">\n    ' + \
  '<rdf:Description rdf:about="#_000002">\n      ' + \
  '<bqbiol:is>\n        <rdf:Bag>\n          ' + \
  '<rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0005623"/>\n        </rdf:Bag>\n      </bqbiol:is>' + \
  '\n   </rdf:Description>\n  </rdf:RDF>\n</annotation>'
result_is = '<bqbiol:is>\n        <rdf:Bag>\n          ' + \
  '<rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0005623"/>\n        </rdf:Bag>\n      </bqbiol:is>'
result_is = result_is.replace("      ", "")

result_wrong = 'This does not have any identifier'


class TestAnnotation(unittest.TestCase):

    def testGetOntAnnotation(self):
      self.assertEqual(af.getOntAnnotation(annotation_isVersionOf), result_isVersionOf)
      self.assertEqual(af.getOntAnnotation(annotation_is), result_is)
      self.assertEqual(af.getOntAnnotation(result_wrong), '')
