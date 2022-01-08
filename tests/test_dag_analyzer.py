# test_dag_analyzer.py
# testing dag_analyzer.py

import libsbml
import numpy as np
import os
import unittest
import sys
from SBMate import constants as cn
from SBMate import sbml_annotation as sa
from SBMate import dag_analyzer as da

BIOMD_12 = 'BIOMD0000000012.xml'

class TestDAGAnalyzer(unittest.TestCase):

  def setUp(self):
    self.sbml_annotation = sa.SBMLAnnotation(file=os.path.join(cn.TEST_DIR, BIOMD_12))
    self.reaction1_annotation = self.sbml_annotation.annotations['Reaction1']
    self.reaction1_analyzer = da.DAGAnalyzer(term_id=['GO:0006402'],
    	                                       ontology='go',
    	                                       object_type=libsbml.Reaction,
                                             qualifier_dict={'GO:0006402': 'isVersionOf'})

  def testFindRoot(self):
    self.assertEqual(self.reaction1_analyzer.findRoot(inp_term='GO:0006402'), 'GO:0008150')
    self.assertEqual(self.reaction1_analyzer.findRoot(inp_term='SBO:000123'), None)

  def testGetConsistency(self):
    self.assertFalse(self.reaction1_analyzer.getConsistency(inp_term=1.0))
    self.assertFalse(self.reaction1_analyzer.getConsistency(inp_term=['GO:0006402', 1]))
    self.assertTrue(self.reaction1_analyzer.getConsistency(inp_term=['GO:0006402']))
    self.assertFalse(self.reaction1_analyzer.getConsistency(inp_term=['GO:0110165']))

  def testGetOneTermSpecificity(self):
    dummy_analyzer = da.DAGAnalyzer(term_id=['SBO:0006402'],
                                    ontology='go',
                                    object_type=libsbml.Reaction,
                                    qualifier_dict={'SBO:0006402': 'is'})
    # should return None if term is inconsistent
    self.assertEqual(dummy_analyzer.getOneTermSpecificity('SBO:0006402'), None)
    self.assertTrue(np.round(self.reaction1_analyzer.getOneTermSpecificity('GO:0006402'), 2), 0.67)

  def testGetSpecificity(self):
    dummy_analyzer1 = da.DAGAnalyzer(term_id=['SBO:0006402'],
                                     ontology='go',
                                     object_type=libsbml.Reaction,
                                     qualifier_dict={'SBO:0006402': 'is'})
    dummy_analyzer2 = da.DAGAnalyzer(term_id=['GO:0006402'],
                                     ontology='go',
                                     object_type=libsbml.Reaction,
                                     qualifier_dict={'GO:0006402': 'isVersionOf'})
    # should return None if term is inconsistent
    self.assertEqual(dummy_analyzer1.getSpecificity(['SBO:0006402']), None)
    self.assertEqual(np.round(dummy_analyzer2.getSpecificity('GO:0006402'), 2), 0.34)
    self.assertEqual(np.round(dummy_analyzer2.getSpecificity(['GO:0006402']), 2), 0.34)
    self.assertEqual(dummy_analyzer2.getSpecificity(['GO:0006402', 'SBO:12345']), None)


if __name__ == '__main__':
  unittest.main()



