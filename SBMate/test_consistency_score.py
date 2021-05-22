# test_consistency_score.py
"""
Tests test_consistency_score.py
# testing
python -m unittest test_consistency_score
"""

import libsbml
import os
import unittest
import consistency_score as cs

class TestConsistencyScore(unittest.TestCase):

  def testFindGORoot(self):
    # molecular function
    self.assertEqual(cs.findGORoot('GO:0004708'), 'GO:0003674')
    # biological process
    self.assertEqual(cs.findGORoot('GO:0035556'), 'GO:0008150')
    # cellular component
    self.assertEqual(cs.findGORoot('GO:0005794'), 'GO:0005575')
    # if not applicable
    self.assertEqual(cs.findGORoot('SBO:0005794'), None)

  def testFindSBORoot(self):
    # mathematical expression
    self.assertEqual(cs.findSBORoot('SBO:0000355'), 'SBO:0000064')
    # occurring entity representation
    self.assertEqual(cs.findSBORoot('SBO:0000375'), 'SBO:0000231')
    # physical entity representationo
    self.assertEqual(cs.findSBORoot('SBO:0000241'), 'SBO:0000236')  
    # if not applicable
    self.assertEqual(cs.findSBORoot('GOO:0000241'), None)

  def testIsGOConsistent(self):
    # a molecular function term with libsbml.Reaction
    self.assertTrue(cs.isGOConsistent('GO:0004708', libsbml.Reaction))
    # a biological process term with libsbml.Model
    self.assertTrue(cs.isGOConsistent('GO:0035556', libsbml.Model))
    # a cellular component term with libsbml.Compartment
    self.assertTrue(cs.isGOConsistent('GO:0005794', libsbml.Compartment))
    # a cellular component term with libsbml.Species
    self.assertTrue(cs.isGOConsistent('GO:0005794', libsbml.Species))

  def testIsSBOConsistent(self):
    # Similar to above
    self.assertTrue(cs.isSBOConsistent('SBO:0000375', libsbml.Reaction))
    self.assertTrue(cs.isSBOConsistent('SBO:0000374', libsbml.Model))
    self.assertTrue(cs.isSBOConsistent('SBO:0000284', libsbml.Compartment))
    self.assertTrue(cs.isSBOConsistent(['SBO:0000241'], libsbml.Species))

  def testISCHEBIConsistent(self):
    # if the term is not in CHEBI tree, for example a GO term is given
    self.assertFalse(cs.isCHEBIConsistent('GO:0035556', libsbml.Reaction))
    # Reaction should not have any CHEBI term
    self.assertFalse(cs.isCHEBIConsistent('CHEBI:28087', libsbml.Reaction))
    # Species can have a correct CHEBI term
    self.assertTrue(cs.isCHEBIConsistent('CHEBI:28087', libsbml.Species))

  def testisUNIPROTConsistent(self):
    self.assertFalse(cs.isUNIPROTConsistent('GO:0035556', libsbml.Reaction))
    self.assertFalse(cs.isUNIPROTConsistent('P0DP23', libsbml.Compartment))
    self.assertTrue(cs.isUNIPROTConsistent(['P0DP23'], libsbml.Species))
    self.assertFalse(cs.isUNIPROTConsistent(['P0DP23', 'C94967'], libsbml.Species))





















