# test_sbml_annotation.py
# testing sbml_annotation.py
# python -m unittest test_sbml_annotation

import libsbml
import os
import unittest
import sys
sys.path.append(os.path.join(os.getcwd(), '../'))
from SBMate import constants as cn
from SBMate import sbml_annotation as sa

BIOMD_12 = 'BIOMD0000000012.xml'

class TestRawSBMLAnnotation(unittest.TestCase):

  def setUp(self):	
    reader = libsbml.SBMLReader()
    document = reader.readSBML(BIOMD_12)
    self.sbml_model = document.getModel()
    self.raw_sbml_annotation = sa.RawSBMLAnnotation(input_file=BIOMD_12)

  def testGetSBOAnnotation(self):
  	# testing annotations obtained from sbo_term
    reaction1_sbo_annotation = self.raw_sbml_annotation.getSBOAnnotation(self.sbml_model.getReaction('Reaction1'))
    self.assertEqual(reaction1_sbo_annotation[0], 'Reaction1')
    self.assertEqual(reaction1_sbo_annotation[1], libsbml.Reaction)
    self.assertEqual(reaction1_sbo_annotation[2], 'SBO:0000179')
    px_sbo_annotation = self.raw_sbml_annotation.getSBOAnnotation(self.sbml_model.getSpecies('PX'))
    self.assertEqual(px_sbo_annotation[0], 'PX')
    self.assertEqual(px_sbo_annotation[1], libsbml.Species)
    self.assertEqual(px_sbo_annotation[2], 'SBO:0000252')

  def testGetOntAnnotation(self):
  	# testing from getAnnotationString()
    reaction1_annotation = self.raw_sbml_annotation.getOntAnnotation(self.sbml_model.getReaction('Reaction1'))
    reaction1_str_annotation = '<bqbiol:isVersionOf>\n  <rdf:Bag>\n    <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0006402"/>\n  </rdf:Bag>\n</bqbiol:isVersionOf>'
    self.assertEqual(reaction1_annotation[0], 'Reaction1')
    self.assertEqual(reaction1_annotation[1], libsbml.Reaction)
    self.assertEqual(reaction1_annotation[2], reaction1_str_annotation)
    # testing for Species
    px_annotation = self.raw_sbml_annotation.getOntAnnotation(self.sbml_model.getSpecies('PX'))
    px_str_annotation = '<bqbiol:is>\n  <rdf:Bag>\n    <rdf:li rdf:resource="http://identifiers.org/uniprot/P03023"/>\n  </rdf:Bag>\n</bqbiol:is>'
    self.assertEqual(px_annotation[0], 'PX')
    self.assertEqual(px_annotation[1], libsbml.Species)
    self.assertEqual(px_annotation[2], px_str_annotation)


class TestSortedSBMLAnnotation(unittest.TestCase):

  def setUp(self):
    self.sbml_annotation = sa.SortedSBMLAnnotation(file=BIOMD_12)
    self.input_annotation = '<bqbiol:isVersionOf>\n  <rdf:Bag>\n    <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0006402"/>\n  </rdf:Bag>\n</bqbiol:isVersionOf>'

  def testGetAnnotationDict(self):
    model_annotation = self.sbml_annotation.getAnnotationDict('BIOMD0000000012')
    self.assertEqual(model_annotation['go'], ['GO:0040029'])
    self.assertEqual(model_annotation['object_id'], 'BIOMD0000000012')
    self.assertEqual(model_annotation['object_type'], libsbml.Model)
    self.assertTrue(model_annotation['sbo'] is None)
    self.assertTrue(model_annotation['chebi'] is None)
    self.assertTrue(model_annotation['kegg_species'] is None)
    self.assertTrue(model_annotation['kegg_process'] is None)
    self.assertTrue(model_annotation['uniprot'] is None)
    px_annotation = self.sbml_annotation.getAnnotationDict('PX')
    self.assertEqual(px_annotation['sbo'], ['SBO:0000252'])
    self.assertEqual(px_annotation['uniprot'], ['P03023'])    

  def testGetKnowledgeResourceTuple(self):
    one_tuple_list = self.sbml_annotation.getKnowledgeResourceTuple(input_annotation=self.input_annotation)
    self.assertEqual(one_tuple_list, [('obo.go', 'GO:0006402')])
    self.assertTrue(self.sbml_annotation.getKnowledgeResourceTuple(None) is None)








