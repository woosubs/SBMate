# test_sbmate_1.py

import copy
import libsbml
import numpy as np
import os
import sys
import unittest
from SBMate import constants as cn
from SBMate import sbmate


BIOMD_12 = 'BIOMD0000000012.xml'
RESULT_REPORT = "Summary of Metrics (BIOMD0000000012.xml)\n----------------------\n" +\
                "annotatable_entities: 20\nannotated_entities: 20\ncoverage: 1.0\n" + \
                "consistent_entities: 19\nconsistency: 0.95\nspecificity: 0.88\n" +\
                "----------------------\n"
IGNORE_TEST = True
IS_PLOT = True
MODEL_FILE = os.path.join(cn.TEST_DIR, BIOMD_12)
ANNOTATION_METRICS = sbmate.AnnotationMetrics(MODEL_FILE)


class TestAnnotatinoMetrics(unittest.TestCase):

  def setUp(self):	
    self.annotation_metrics = copy.deepcopy(ANNOTATION_METRICS)

  def testInit(self):
    if IGNORE_TEST:
        return
    df = self.annotation_metrics.metrics_df
    self.assertEqual(df.shape, (1,6))
    self.assertEqual(df.index[0], MODEL_FILE)
    self.assertEqual(int(df['annotatable_entities']), 20)
    self.assertEqual(int(df['annotated_entities']), 20)
    self.assertEqual(float(df['coverage']), 1.0)
    self.assertEqual(int(df['consistent_entities']), 19)
    self.assertEqual(float(df['consistency']), 0.95)
    self.assertEqual(float(df['specificity']), 0.88)

  def testGetMetrics(self):
    # TESTING
    self.res_report = sbmate.AnnotationMetrics.getMetrics(MODEL_FILE,
        output="report")
    self.res_df = self.annotation_metrics.getMetrics(MODEL_FILE,
        output="table")
    self.res_none = self.annotation_metrics.getMetrics(
        123, output="table")
    self.res_none2 = self.annotation_metrics.getMetrics(
        [123, 'abc'], output="table")
    self.assertEqual(self.res_report, RESULT_REPORT)
    self.assertEqual(self.res_df.shape, (1,6))
    self.assertEqual(self.res_none, None)
    self.assertEqual(self.res_none2, None)

  def testGetMetricsReport(self):
    if IGNORE_TEST:
      return
    report = sbmate._getMetricsReport()
    self.assertEqual(report, RESULT_REPORT)

  def testMetricsTable(self):
    if IGNORE_TEST:
      return
    df = self.annotation_metrics.metrics_df
    self.assertEqual(df.shape, (1,6))
    self.assertEqual(df.index[0], BIOMD_12)
    self.assertEqual(int(df['annotatable_entities']), 20)
    self.assertEqual(int(df['annotated_entities']), 20)
    self.assertEqual(float(df['coverage']), 1.0)
    self.assertEqual(int(df['consistent_entities']), 19)
    self.assertEqual(float(df['consistency']), 0.95)
    self.assertEqual(float(df['specificity']), 0.88)


if __name__ == '__main__':
  unittest.main()
