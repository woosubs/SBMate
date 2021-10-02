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
RESULT_REPORT_ENTRIES = [
    "annotatable_entities: 20",
    "annotated_entities: 20",
    "coverage: 1.0",
    "consistent_entities: 19",
    "consistency: 0.9",
    "specificity: 0.88",
    BIOMD_12,
    ]
IGNORE_TEST = False
IS_PLOT = False
MODEL_FILE = os.path.join(cn.TEST_DIR, BIOMD_12)
ANNOTATION_METRICS = sbmate.AnnotationMetrics(MODEL_FILE)

METRIC_NAMES = [
    'annotatable_entities',
    'annotated_entities',
    'coverage',
    'consistent_entities',
    'consistency',
    'specificity',
    ]


class TestAnnotatinoMetrics(unittest.TestCase):

  def setUp(self):	
    self.annotation_metrics = copy.deepcopy(ANNOTATION_METRICS)

  def testInit(self):
    if IGNORE_TEST:
        return
    df = self.annotation_metrics.metrics_df

  def testTwoClasses(self):
    if IGNORE_TEST:
      return
    annotation_metrics = sbmate.AnnotationMetrics(MODEL_FILE,
        metric_calculator_classes=[MetricCalculator])
    df = annotation_metrics.metrics_df
    lst = df.columns.tolist()
    for name in METRIC_NAMES:
      self.assertEqual(lst.count(name), 2)

  def basicChecks(self, df):
    self.assertEqual(df.shape, (1,6))
    self.assertEqual(df.index[0], BIOMD_12)
    self.assertEqual(int(df['annotatable_entities']), 20)
    self.assertEqual(int(df['annotated_entities']), 20)
    self.assertEqual(float(df['coverage']), 1.0)
    self.assertEqual(int(df['consistent_entities']), 19)
    self.assertEqual(float(df['consistency']), 0.95)
    self.assertEqual(float(df['specificity']), 0.88)

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
    res_none = self.annotation_metrics.getMetrics(
        123, output="table")
    res_none2 = self.annotation_metrics.getMetrics(
        [123, 'abc'], output="table")
    self.assertEqual(res_df.shape, (1,6))
    self.assertEqual(res_none, None)
    self.assertEqual(res_none2, None)

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
    self.assertEqual(int(df['annotatable_entities']), 20)
    self.assertEqual(int(df['annotated_entities']), 20)
    self.assertEqual(float(df['coverage']), 1.0)
    self.assertEqual(int(df['consistent_entities']), 19)
    self.assertEqual(float(df['consistency']), 0.95)
    self.assertEqual(float(df['specificity']), 0.88)


if __name__ == '__main__':
  unittest.main()
