# test_sbmate.py
# test sbmate class-
# python -m unittest test_sbmate

import libsbml
import numpy as np
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import unittest
from SBMate import constants as cn
from SBMate import sbmate

BIOMD_12 = 'BIOMD0000000012.xml'
RESULT_REPORT = "Model \'BIOMD0000000012.xml\' has total 20 annotatable entities.\n20 " + \
                "entities are annotated.\n19 entities are consistent." +\
                "\n...\nCoverage is: 1.00\nConsistency is: 0.95\nSpecificity is: 0.88\n"

class TestSBMate(unittest.TestCase):

  def setUp(self):	
    self.metrics_class = sbmate.AnnotationMetrics(model_file=os.path.join(cn.TEST_DIR, BIOMD_12))

  def testGetCoverage(self):
  	anot_entities, coverage = self.metrics_class.getCoverage()
  	self.assertEqual(len(anot_entities), 20)
  	self.assertTrue('BIOMD0000000012' in anot_entities)
  	self.assertEqual(self.metrics_class.coverage, 1.0)

  def testGetConsistency(self):
    consist_entities, consistency = self.metrics_class.getConsistency(self.metrics_class.consistent_entities)
    self.assertEqual(len(consist_entities.keys()), 19)
    self.assertFalse('cell' in consist_entities.keys())
    self.assertEqual(self.metrics_class.consistency, 0.95)
    none_consist_entities, none_consistency = self.metrics_class.getConsistency([])
    self.assertEqual(none_consist_entities, None)
    self.assertEqual(none_consistency, None)

  def testGetSpecificity(self):
    specificity = self.metrics_class.getSpecificity(self.metrics_class.consistent_entities)
    self.assertEqual(specificity, 0.88)
    # case for 'None'
    none_specificity = self.metrics_class.getSpecificity(dict())
    self.assertEqual(none_specificity, None)


class TestFunctions(unittest.TestCase):

  def setUp(self):
    self.res_report = sbmate.getMetrics(os.path.join(cn.TEST_DIR, BIOMD_12), output="report")
    self.res_df = sbmate.getMetrics(os.path.join(cn.TEST_DIR, BIOMD_12), output="table")
    self.res_none = sbmate.getMetrics(123, output="table")
    self.res_none2 = sbmate.getMetrics([123, 'abc'], output="table")

  def testGetMetrics(self):
    self.assertEqual(self.res_report, RESULT_REPORT)
    self.assertEqual(self.res_df.shape, (1,6))
    self.assertEqual(self.res_none, None)
    self.assertEqual(self.res_none2, None)

  def testGetMetricsReport(self):
    report = sbmate.getMetricsReport(('BIOMD0000000012.xml', sbmate.AnnotationMetrics(model_file=os.path.join(cn.TEST_DIR, BIOMD_12))))
    self.assertEqual(report, self.res_report)

  def testGetMetricsTable(self):
    df = sbmate.getMetricsTable(('BIOMD0000000012.xml', sbmate.AnnotationMetrics(model_file=os.path.join(cn.TEST_DIR, BIOMD_12))))
    self.assertEqual(set(df.index), {'BIOMD0000000012.xml'})
    self.assertEqual(list(df.iloc[0]), [20, 20, 19, '1.00', '0.95', '0.88'])




if __name__ == '__main__':
  unittest.main()