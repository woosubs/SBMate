# test_sbml_annotation.py
# testing sbml_annotation.py
# python -m unittest test_sbml_annotation

import libsbml
import unittest
import constants as cn
import sbml_annotation as sa

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