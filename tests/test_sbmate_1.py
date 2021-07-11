# test_sbmate_1.py

import libsbml
import numpy as np
import os
import sys
import unittest
from SBMate import constants as cn
from SBMate import sbmate_1 as sbmate


BIOMD_12 = 'BIOMD0000000012.xml'
RESULT_REPORT = "Summary of Metrics (BIOMD0000000012.xml)\n----------------------\n" +\
                "annotatable_entities: 20\nannotated_entities: 20\ncoverage: 1.0\n" + \
                "consistent_entities: 19\nconsistency: 0.95\nspecificity: 0.88\n" +\
                "----------------------\n"


class TestAnnotatinoMetrics(unittest.TestCase):

  def setUp(self):	
    self.metrics_class = sbmate.AnnotationMetrics(model_file=os.path.join(cn.TEST_DIR, BIOMD_12))

  def testInit(self):
    df = self.metrics_class.metrics_df
    self.assertEqual(df.shape, (1,6))
    self.assertEqual(df.index[0], BIOMD_12)
    self.assertEqual(int(df['annotatable_entities']), 20)
    self.assertEqual(int(df['annotated_entities']), 20)
    self.assertEqual(float(df['coverage']), 1.0)
    self.assertEqual(int(df['consistent_entities']), 19)
    self.assertEqual(float(df['consistency']), 0.95)
    self.assertEqual(float(df['specificity']), 0.88)


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
  	pass

  def testGetMetricsTable(self):
    pass

if __name__ == '__main__':
  unittest.main()






