# test_uniprot_kegg_analyzer.py

import libsbml
import numpy as np
import os
import unittest
import sys
from SBMate import constants as cn
from SBMate import sbml_annotation as sa
from SBMate import uniprot_kegg_analyzer as uka

BIOMD_12 = 'BIOMD0000000012.xml'
BIOMD_13 = 'BIOMD0000000013.xml'


class TestNonDAGAnalyzer(unittest.TestCase):

  def setUp(self):
    self.biomd12 = sa.SortedSBMLAnnotation(file=os.path.join(cn.TEST_DIR, BIOMD_12))
    self.px_annotation = self.biomd12.annotations['PX']
    self.px_analyzer = uka.NonDAGAnalyzer(term_id=['P03023'],
                                          ontology='uniprot',
                                          object_type=libsbml.Species)
    self.x_annotation = self.biomd12.annotations['X']
    self.x_analyzer = uka.NonDAGAnalyzer(term_id=['C00046'],
                                         ontology='kegg_species',
                                         object_type=libsbml.Species)


  def testGetOneTermConsistency(self):
    self.assertTrue(self.x_analyzer.getOneTermConsistency('C00046'))
    self.assertFalse(self.x_analyzer.getOneTermConsistency('GO:12345'))
    self.assertTrue(self.px_analyzer.getOneTermConsistency('P03023'))
    self.assertFalse(self.px_analyzer.getOneTermConsistency('GO:12345'))  

  def testGetConsistency(self):
    self.assertFalse(self.x_analyzer.getConsistency(1.0))
    self.assertFalse(self.x_analyzer.getConsistency('GO:ABC'))
    self.assertTrue(self.x_analyzer.getConsistency(['C00046']))
    self.assertFalse(self.x_analyzer.getConsistency(['C00046', 1.0]))
    self.assertFalse(self.x_analyzer.getConsistency(['C00046', 'GO:ABC']))

  def testGetSpecificity(self):
  	wrong_analyzer = uka.NonDAGAnalyzer(term_id=['GO:12345'],
                                         ontology='kegg_species',
                                         object_type=libsbml.Species)
  	self.assertEqual(wrong_analyzer.getSpecificity('GO:12345'), None)
  	self.assertEqual(self.x_analyzer.getSpecificity('C00046'), 1.0)
  	self.assertEqual(self.px_analyzer.getSpecificity('P03023'), 1.0)


if __name__ == '__main__':
  unittest.main()