# test_metric_calculator.py

import libsbml
import networkx as nx
import numpy as np
import os
import pandas as pd
import re
import requests
import unittest
from SBMate import constants as cn
from SBMate import metric_calculator as mc
from SBMate import sbml_annotation as sa


BIOMD_12 = 'BIOMD0000000012.xml'
BIOMD_970 = 'BIOMD0000000970.xml'


class TestMetricCalculator(unittest.TestCase):

  def setUp(self):	
    self.one_annotation = sa.SortedSBMLAnnotation(file=os.path.join(cn.TEST_DIR, BIOMD_12))
    self.two_annotation = sa.SortedSBMLAnnotation(file=os.path.join(cn.TEST_DIR, BIOMD_970))
    self.calculator = mc.MetricCalculator(annotations=self.one_annotation, model_name=BIOMD_12)
    self.none_calculator = mc.MetricCalculator(annotations=self.two_annotation, model_name=BIOMD_970)

  def testCalculate(self):
    metrics_df = self.calculator.calculate()
    self.assertEqual(metrics_df.index[0], BIOMD_12)
    self.assertEqual(metrics_df.shape, (1,6))
    self.assertEqual(int(metrics_df['annotatable_entities']), 20)
    self.assertEqual(int(metrics_df['annotated_entities']), 20)
    self.assertEqual(float(metrics_df['coverage']), 1.0)
    self.assertEqual(int(metrics_df['consistent_entities']), 19)
    self.assertEqual(float(metrics_df['consistency']), 0.95)
    self.assertEqual(float(metrics_df['specificity']), 0.88)
    #
    non_metrics_df = self.none_calculator.calculate()
    self.assertEqual(non_metrics_df.index[0], BIOMD_970)
    self.assertEqual(non_metrics_df.shape, (1,6))
    self.assertEqual(int(non_metrics_df['annotatable_entities']), 10)
    self.assertEqual(non_metrics_df['annotated_entities'][0], None)
    self.assertEqual(float(non_metrics_df['coverage']), 0.0)
    self.assertEqual(non_metrics_df['consistent_entities'][0], None)
    self.assertEqual(non_metrics_df['consistency'][0], None)
    self.assertEqual(non_metrics_df['specificity'][0], None)

  def testMkDataframe(self):
    df = self.calculator.mkDataframe({'one_val': 10})
    self.assertEqual(df.shape, (1,1))
    self.assertEqual(df.index[0], BIOMD_12)
    self.assertEqual(int(df['one_val']), 10)

  def testGetCoverage(self):
    annotated_entities, coverage = self.calculator._getCoverage()
    self.assertEqual(len(annotated_entities), 20)
    self.assertEqual(coverage, 1.0)
    self.assertEqual(set(annotated_entities), set(self.one_annotation.annotations.keys()))
    #
    none_annotated_entities, none_coverage = self.none_calculator._getCoverage()
    self.assertEqual(none_annotated_entities, [])
    self.assertEqual(none_coverage, 0.0)

  def testGetConsistency(self):
    annotated_entities, coverage = self.calculator._getCoverage()
    consistent_entities, consistency = self.calculator._getConsistency(annotated_entities)
    self.assertEqual(len(consistent_entities), 19)
    self.assertEqual(consistency, 0.95)
    self.assertFalse('cell' in set(consistent_entities))
    #
    none_annotated_entities, none_coverage = self.none_calculator._getCoverage()
    none_consistent_entities, none_consistency = self.none_calculator._getConsistency(none_annotated_entities)
    self.assertEqual(none_consistent_entities, None)
    self.assertEqual(none_consistency, None)

  def testGetSpecificity(self):
    annotated_entities, coverage = self.calculator._getCoverage()
    consistent_entities, consistency = self.calculator._getConsistency(annotated_entities)
    specificity = self.calculator._getSpecificity(consistent_entities) 
    self.assertEqual(specificity, 0.88)
    #
    none_annotated_entities, none_coverage = self.none_calculator._getCoverage()
    none_consistent_entities, none_consistency = self.none_calculator._getConsistency(none_annotated_entities)
    none_specificity = self.none_calculator._getSpecificity(none_consistent_entities)
    self.assertEqual(none_specificity, None)


if __name__ == '__main__':
  unittest.main() 	


