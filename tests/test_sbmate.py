# test_sbmate_1.py

import copy
import libsbml
import numpy as np
import os
import sys
import unittest
from SBMate import constants as cn
from SBMate.metric_calculator import MetricCalculator
from SBMate import sbmate


BIOMD_12 = 'BIOMD0000000012.xml'
BIOMD_13 = 'BIOMD0000000013.xml'
RESULT_REPORT_ENTRIES = [
    "annotatable_elements: 20",
    "annotated_elements: 20",
    "coverage: 1.0",
    "consistent_elements: 19",
    "consistency: 0.9",
    "specificity: 0.7",
    BIOMD_12,
    ]
IGNORE_TEST = False
IS_PLOT = False
MODEL_FILE = os.path.join(cn.TEST_DIR, BIOMD_12)
MODEL_FILE2 = os.path.join(cn.TEST_DIR, BIOMD_13)
ANNOTATION_METRICS = sbmate.AnnotationMetrics(MODEL_FILE)

METRIC_NAMES = [
    'annotatable_elements',
    'annotated_elements',
    'coverage',
    'consistent_elements',
    'consistency',
    'specificity',
    ]


class TestAnnotatinoMetrics(unittest.TestCase):

  def setUp(self):	
    self.annotation_metrics = copy.deepcopy(ANNOTATION_METRICS)
    self.no_annotation_metrics = sbmate.AnnotationMetrics()

  def testInit(self):
    if IGNORE_TEST:
        return
    df = self.annotation_metrics.metrics_df
    self.assertEqual(self.no_annotation_metrics.annotations, None)
    self.assertEqual(self.no_annotation_metrics.metrics_df, None)

  def testTwoClasses(self):
    if IGNORE_TEST:
      return
    one_annotation_metrics = sbmate.AnnotationMetrics(MODEL_FILE,
        metric_calculator_classes=[MetricCalculator])
    df = one_annotation_metrics.metrics_df
    lst = df.columns.tolist()
    for name in METRIC_NAMES:
      self.assertEqual(lst.count(name), 2)

  def basicChecks(self, df):
    self.assertEqual(df.shape, (1,6))
    self.assertEqual(df.index[0], BIOMD_12)
    self.assertEqual(int(df['annotatable_elements']), 20)
    self.assertEqual(int(df['annotated_elements']), 20)
    self.assertEqual(float(df['coverage']), 1.0)
    self.assertEqual(int(df['consistent_elements']), 19)
    self.assertEqual(float(df['consistency']), 0.95)
    self.assertEqual(float(df['specificity']), 0.7)

  def testInit(self):
    if IGNORE_TEST:
        return
    df = self.annotation_metrics.metrics_df
    self.basicChecks(df)

  def testGetMetrics(self):
    if IGNORE_TEST:
        return
    res_report = sbmate.AnnotationMetrics.getMetrics(MODEL_FILE,
        output="report")
    self.checkReport(report=res_report)
    res_df = self.annotation_metrics.getMetrics(MODEL_FILE,
        output="table")
    self.assertEqual(res_df.shape, (1,6))
    self.assertEqual(int(res_df['annotatable_elements']), 20)
    self.assertEqual(int(res_df['annotated_elements']), 20)
    self.assertEqual(float(res_df['coverage']), 1.0)
    self.assertEqual(int(res_df['consistent_elements']), 19)
    self.assertEqual(float(res_df['consistency']), 0.95)
    self.assertEqual(float(res_df['specificity']), 0.7) 

    res_df2 = self.annotation_metrics.getMetrics([MODEL_FILE, MODEL_FILE2], 
                                                  output="table")
    self.assertEqual(res_df2.shape, (2,6))
    self.assertEqual(list(res_df2.columns), METRIC_NAMES)
    self.assertEqual(list(res_df2.loc[BIOMD_12,:]),
                     [20, 20, 1.0, 19, 0.95, 0.7])
    self.assertEqual(list(res_df2.loc[BIOMD_13,:]),
                     [51, 51, 1.0, 51, 1.00, 0.93])
    
    res_report =  self.annotation_metrics.getMetrics(MODEL_FILE,
        output="report")
    self.assertEqual(res_report, self.annotation_metrics._getMetricsReport())
    with self.assertRaises(ValueError) as context: 
      self.annotation_metrics.getMetrics(123, output="table")
    with self.assertRaises(ValueError) as context: 
      self.annotation_metrics.getMetrics([123, 'abc'], output="table")

    with self.assertRaisesRegex(ValueError, "Should be a valid file name."): 
      self.annotation_metrics.getMetrics(123, output="table")  
    with self.assertRaisesRegex(ValueError, "Should be a valid file name."): 
      self.annotation_metrics.getMetrics([123, 'abc'], output="table")  

  def checkReport(self, report=None):
    if report is None:
      report = self.annotation_metrics._getMetricsReport()
    report = self.annotation_metrics._getMetricsReport()
    trues = [e in report for e in RESULT_REPORT_ENTRIES]
    self.assertTrue(all(trues))

  def testGetMetricsReport(self):
    if IGNORE_TEST:
        return
    self.checkReport()

  def testMetricsTable(self):
    if IGNORE_TEST:
      return
    df = self.annotation_metrics.metrics_df
    self.assertEqual(df.shape, (1,6))
    self.assertEqual(int(df['annotatable_elements']), 20)
    self.assertEqual(int(df['annotated_elements']), 20)
    self.assertEqual(float(df['coverage']), 1.0)
    self.assertEqual(int(df['consistent_elements']), 19)
    self.assertEqual(float(df['consistency']), 0.95)
    self.assertEqual(float(df['specificity']), 0.7)


if __name__ == '__main__':
  unittest.main()
