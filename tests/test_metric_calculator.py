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

class TestMetricCalculator(unittest.TestCase):

  def setUp(self):	
    self.one_annotation = sa.SortedSBMLAnnotation(file=BIOMD_12)
    self.calculator = mc.MetricCalculator(annotations=self.one_annotation, file=BIOMD_12)

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

  def testMkDataframe(self):
    df = self.calculator.mkDataframe({'one_val': 10})
    self.assertEqual(df.shape, (1,1))
    self.assertEqual(df.index[0], BIOMD_12)
    self.assertEqual(int(df['one_val']), 10)

  def testGetCoverage(self):
    annotated_entities, coverage = self.calculator._getCoverage()
    self.assertEqual(len(annotated_entities), 20)
    self.assertEqual(coverage, 1.0)