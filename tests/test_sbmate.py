# test_sbmate.py
# test sbmate class-
# python -m unittest test_sbmate

import libsbml
import numpy as np
import os
import sys
sys.path.append(os.path.join(os.getcwd(), '../'))
import unittest
from SBMate import constants as cn
from SBMate import sbmate

BIOMD_12 = 'BIOMD0000000012.xml'
RESULT_REPORT = "Model has total 20 annotatable entities.\n20 " + \
                "entities are annotated.\n19 entities are consistent." +\
                "\n...\nCoverage is: 1.00\nConsistency is: 0.95\nSpecificity is: 0.88\n"

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


class TestFunctions(unittest.TestCase):

  def setUp(self):
    self.res_report = sbmate.getMetrics(BIOMD_12, output="report")
    self.res_df = sbmate.getMetrics(BIOMD_12, output="table")

  def testGetMetrics(self):
    self.assertEqual(self.res_report, RESULT_REPORT)
    self.assertEqual(self.res_df.shape, (1,6))
