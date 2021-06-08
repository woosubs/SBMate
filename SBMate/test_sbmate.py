# test_sbmate.py
# test sbmate class-
# python -m unittest test_sbmate

import libsbml
import numpy as np
import unittest
import constants as cn
import sbmate

BIOMD_12 = 'BIOMD0000000012.xml'

class TestSBMate(unittest.TestCase):

  def setUp(self):	
    self.metrics_class = sbmate.AnnotationMetrics(model_file=BIOMD_12)

  def testGetCoverage(self):
  	anot_entities, coverage = self.metrics_class.getCoverage()
  	self.assertEqual(len(anot_entities), 20)
  	self.assertTrue('BIOMD0000000012' in anot_entities)
  	self.assertEqual(self.metrics_class.coverage, 1.0)

  def testGetConsistency(self):
  	consist_entities, consistency = self.metrics_class.getConsistency(self.metrics_class.consistent_entities)
  	self.assertEqual(len(consist_entities), 19)
  	self.assertFalse('cell' in consist_entities)
  	self.assertEqual(self.metrics_class.consistency, 0.95)

  def testGetSpecificity(self):
  	specificity = self.metrics_class.getSpecificity(self.metrics_class.consistent_entities)
  	self.assertEqual(np.round(specificity, 2),0.88)