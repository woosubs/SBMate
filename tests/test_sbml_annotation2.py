# test_sbml_annotation2.py
# testing sbml_annotation.py
# python -m unittest test_sbml_annotation

import libsbml
import os
import unittest
import sys
from SBMate import constants as cn
from SBMate import sbml_annotation2 as sa

BIOMD_12 = 'BIOMD0000000012.xml'
BIOMD_15 = 'BIOMD0000000015.xml'


class TestRawSBMLAnnotation(unittest.TestCase):

  def setUp(self):	
    reader = libsbml.SBMLReader()
    document = reader.readSBML(os.path.join(cn.TEST_DIR, BIOMD_12))
    self.sbml_model = document.getModel()
    self.raw_sbml_annotation = sa.RawSBMLAnnotation(input_file=os.path.join(cn.TEST_DIR, BIOMD_12))
    # BIOMD13 is for checking incompelte annotation 
    incomplete_document = reader.readSBML(os.path.join(cn.TEST_DIR, BIOMD_15))
    self.incompelte_sbml_model = incomplete_document.getModel()
    self.incomplete_raw_sbml_annotation = sa.RawSBMLAnnotation(input_file=os.path.join(cn.TEST_DIR, BIOMD_15))

  def testFormatSBO(self):
    self.assertEqual(self.raw_sbml_annotation.formatSBO(-1), None)
    self.assertEqual(self.raw_sbml_annotation.formatSBO(179), 'SBO:0000179')

  def testGetSBOAnnotation(self):
  	# testing annotations obtained from sbo_term
    reaction1_sbo_annotation = self.raw_sbml_annotation.getSBOAnnotation(self.sbml_model.getReaction('Reaction1'))
    self.assertEqual(reaction1_sbo_annotation.id, 'Reaction1')
    self.assertEqual(reaction1_sbo_annotation.object_type, libsbml.Reaction)
    self.assertEqual(reaction1_sbo_annotation.annotation, 'SBO:0000179')
    px_sbo_annotation = self.raw_sbml_annotation.getSBOAnnotation(self.sbml_model.getSpecies('PX'))
    self.assertEqual(px_sbo_annotation.id, 'PX')
    self.assertEqual(px_sbo_annotation.object_type, libsbml.Species)
    self.assertEqual(px_sbo_annotation.annotation, 'SBO:0000252')
    # case when SBO doesn't exist
    no_sbo_annotation = self.incomplete_raw_sbml_annotation.getSBOAnnotation(self.incompelte_sbml_model.getSpecies('ATP'))
    self.assertEqual(no_sbo_annotation.id, 'ATP')
    self.assertEqual(no_sbo_annotation.object_type, libsbml.Species)
    self.assertEqual(no_sbo_annotation.annotation, None)

  def testGetOntAnnotation(self):
    # testing from getAnnotationString()
    reaction1_annotation = self.raw_sbml_annotation.getOntAnnotation(self.sbml_model.getReaction('Reaction1'))
    reaction1_str_annotation = '<bqbiol:isVersionOf>\n        <rdf:Bag>\n          '
    reaction1_str_annotation = reaction1_str_annotation + '<rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0006402"/>\n        </rdf:Bag>\n      </bqbiol:isVersionOf>'
    self.assertEqual(reaction1_annotation.id, 'Reaction1')
    self.assertEqual(reaction1_annotation.object_type, libsbml.Reaction)
    self.assertEqual(reaction1_annotation.annotation['isVersionOf'][0], reaction1_str_annotation)
    # testing for Species
    px_annotation = self.raw_sbml_annotation.getOntAnnotation(self.sbml_model.getSpecies('PX'))
    px_str_annotation = '<bqbiol:is>\n        <rdf:Bag>\n          <rdf:li rdf:resource="http://identifiers.org/uniprot/P03023"/>\n        </rdf:Bag>\n      </bqbiol:is>'
    self.assertEqual(px_annotation.id, 'PX')
    self.assertEqual(px_annotation.object_type, libsbml.Species)
    self.assertEqual(px_annotation.annotation['is'][0], px_str_annotation)
    # case when string annotation doesn't exist
    no_ont_annotation = self.incomplete_raw_sbml_annotation.getOntAnnotation(self.incompelte_sbml_model.getSpecies('ATP'))
    self.assertEqual(no_ont_annotation.id, 'ATP')
    self.assertEqual(no_ont_annotation.object_type, libsbml.Species)
    self.assertEqual(no_ont_annotation.annotation, {}) 


class TestSBMLAnnotation(unittest.TestCase):

  def setUp(self):
    self.sbml_annotation = sa.SBMLAnnotation(file=os.path.join(cn.TEST_DIR, BIOMD_12))
    self.input_annotation = '<bqbiol:isVersionOf>\n  <rdf:Bag>\n    <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0006402"/>\n  </rdf:Bag>\n</bqbiol:isVersionOf>'

  def testGetAnnotationDictByQualifier(self):
    model_annotation = self.sbml_annotation.getAnnotationDictByQualifier('BIOMD0000000012')
    self.assertFalse('is' in model_annotation.keys())
    self.assertEqual(model_annotation['object_id'], 'BIOMD0000000012')
    self.assertEqual(model_annotation['object_type'], libsbml.Model)
    self.assertEqual(model_annotation['isVersionOf'],  [('obo.go', 'GO:0040029')])
    #
    px_annotation = self.sbml_annotation.getAnnotationDictByQualifier('PX')
    self.assertFalse('isVersionOf' in px_annotation.keys())
    self.assertTrue(('uniprot', 'P03023') in px_annotation['is'])
    self.assertTrue(('sbo', 'SBO:0000252') in px_annotation['is'])
    self.assertEqual(px_annotation['object_id'],  'PX')
    self.assertEqual(px_annotation['object_type'], libsbml.Species)

  def testGetAnnotationDictByOntology(self):
    model_annotation = self.sbml_annotation.getAnnotationDictByQualifier('BIOMD0000000012')
    px_annotation = self.sbml_annotation.getAnnotationDictByQualifier('PX')
    model_anot_by_ont = self.sbml_annotation.getAnnotationDictByOntology(model_annotation)
    px_anot_by_ont = self.sbml_annotation.getAnnotationDictByOntology(px_annotation)
    self.assertEqual(model_anot_by_ont['go'], ['GO:0040029'])
    self.assertEqual(model_anot_by_ont['object_id'], 'BIOMD0000000012')
    self.assertEqual(model_anot_by_ont['object_type'], libsbml.Model)
    self.assertEqual(px_anot_by_ont['sbo'], ['SBO:0000252'])
    self.assertEqual(px_anot_by_ont['uniprot'], ['P03023'])
    self.assertEqual(px_anot_by_ont['object_id'], 'PX')
    self.assertEqual(px_anot_by_ont['object_type'], libsbml.Species)

  def testGetKnowledgeResourceTuple(self):
    self.assertEqual(self.sbml_annotation.getKnowledgeResourceTuple(self.input_annotation), [('obo.go', 'GO:0006402')])
    self.assertEqual(self.sbml_annotation.getKnowledgeResourceTuple('None'), [])

if __name__ == '__main__':
  unittest.main()





