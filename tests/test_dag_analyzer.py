# test_dag_analyzer.py
# testing dag_analyzer.py

import libsbml
import os
import unittest
import sys
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from SBMate import constants as cn
from SBMate import sbml_annotation as sa
from SBMate import dag_analyzer as da

BIOMD_12 = 'BIOMD0000000012.xml'

class TestSortedSBMLAnnotation(unittest.TestCase):

  def setUp(self):
    self.sbml_annotation = sa.SortedSBMLAnnotation(file=os.path.join(cn.TEST_DIR, BIOMD_12))
    self.reaction1_annotation = self.sbml_annotation.annotations['Reaction1']
    self.reaction1_analyzer = da.DAGAnalyzer(term_id=['GO:0006402'],
    	                                     ontology='go',
    	                                     object_type=libsbml.Reaction)

  def testFindRoot(self):
    self.assertEqual(self.reaction1_analyzer.findRoot(inp_term='GO:0006402'), 'GO:0008150')
    self.assertEqual(self.reaction1_analyzer.findRoot(inp_term='SBO:000123'), None)

  def testGetConsistency(self):
    self.assertFalse(self.reaction1_analyzer.getConsistency(inp_term=1.0))
    self.assertFalse(self.reaction1_analyzer.getConsistency(inp_term=['GO:0006402', 1]))
    self.assertTrue(self.reaction1_analyzer.getConsistency(inp_term=['GO:0006402']))

if __name__ == '__main__':
  unittest.main()



