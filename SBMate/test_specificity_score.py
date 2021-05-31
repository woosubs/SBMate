# test_specificity_score.py
"""
Test specificity_score.py
# testing
python -m unittest test_specificity_score
"""

import libsbml
import os
import unittest
import consistency_score as cs
import specificity_score as ss

class TestSpecificityScore(unittest.TestCase):
  
  def testGetOneSBOSpecificity(self):
    # root term should have 0.0
    self.assertEqual(ss.getOneSBOSpecificity('SBO:0000000'), 0.0)
    # a leaf should have 1.0
    self.assertEqual(ss.getOneSBOSpecificity('SBO:0000553'), 1.0)

  def testGetSBOSpecificity(self):
    # a single string case
    self.assertEqual(ss.getSBOSpecificity('SBO:0000000'), 0.0)
    # a list of two elements
    self.assertEqual(ss.getSBOSpecificity(['SBO:0000000', 'SBO:0000553']), 0.5)

  def testGetOneGOSpecificity(self):
    # root term should have 0.0
    self.assertEqual(ss.getOneGOSpecificity('GO:0008150'), 0.0)
    self.assertEqual(ss.getOneGOSpecificity('GO:0003674'), 0.0)
    self.assertEqual(ss.getOneGOSpecificity('GO:0005575'), 0.0)
    # a leaf should have 1.0
    self.assertEqual(ss.getOneGOSpecificity('GO:0048096'), 1.0)

  def testGetGOSpecificity(self):
    # a single string case
    self.assertEqual(ss.getGOSpecificity('GO:0008150'), 0.0)
    # a list of two elements
    self.assertEqual(ss.getGOSpecificity(['GO:0008150', 'GO:0048096']), 0.5)

  def testGetOneCHEBISpecificity(self):
    # root term should have 0.0
    self.assertEqual(ss.getOneCHEBISpecificity('CHEBI:24431'), 0.0)
    # a leaf should have 1.0
    self.assertEqual(ss.getOneCHEBISpecificity('CHEBI:28087'), 1.0)

  def testGetCHEBISpecificity(self):
    # a single string case
    self.assertEqual(ss.getCHEBISpecificity('CHEBI:24431'), 0.0)
    # a list of two elements
    self.assertEqual(ss.getCHEBISpecificity(['CHEBI:24431', 'CHEBI:28087']), 0.5)

  def testGetOthersSpecificity(self):
    self.assertEqual(ss.getOthersSpecificity(['P0DP23']), 1.0)
    self.assertEqual(ss.getOthersSpecificity('C00062'), 1.0)