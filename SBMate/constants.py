# constants.py
"""
Constants for modlues
"""

import libsbml
import os

PROJECT_NAME = "SBMate"

# folders
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
# one level higher
PROJECT_DIR = os.path.dirname(PROJECT_DIR)
RESOURCE_DIR = os.path.join(PROJECT_DIR, "knowledge_resources")
TEST_DIR = os.path.join(PROJECT_DIR, "tests")


# Model entity types
MODEL = libsbml.Model
REACTION = libsbml.Reaction
SPECIES = libsbml.Species
COMPARTMENT = libsbml.Compartment
BIOL_PROC = 'biological_process'
MOLE_FUNC = 'molecular_function'
CELL_COMP = 'cellular_component'
# GO term ids matching the above names
GO_BIO_PROC = "GO:0008150"
GO_MOL_FUNC = "GO:0003674"
GO_CELL_COMP = "GO:0005575"
# GO_PARENTS = [GO_BIO_PROC, GO_MOL_FUNC, GO_CELL_COMP]
GO_ROOTS = [GO_BIO_PROC, GO_MOL_FUNC, GO_CELL_COMP]

BIOMODEL_OBJECTS = [MODEL,
                    REACTION,
                    SPECIES,
                    COMPARTMENT,
                   ]
OBJECT_GO_MAP = {MODEL: {BIOL_PROC, MOLE_FUNC},
                 REACTION: {BIOL_PROC, MOLE_FUNC},
                 SPECIES: {CELL_COMP},
                 COMPARTMENT: {CELL_COMP},
                }
GO_ROOT_DICT = {GO_BIO_PROC: BIOL_PROC,
                GO_MOL_FUNC: MOLE_FUNC,
                GO_CELL_COMP: CELL_COMP,
                None: "None"
                }

# Knowledge resource identifiers for URI
GOS = {'go', 'GO', 'obo.go'}
SBOS = {'biomodels.sbo', 'sbo'}
CHEBIS = {'chebi', 'obo.chebi'}
KEGG_SPEC = {'kegg.compound',
             'kegg.genes',
             'kegg.drug',
             'kegg.orthology'}
KEGG_PROC= {'kegg.reaction',
            'kegg.pathway'}
UNIPROTS = {'uniprot', 'uniprot.isoform'}

ALL_KNOWLEDGE_TYPES = set.union(*[GOS, SBOS, CHEBIS,
                                  KEGG_SPEC, KEGG_PROC,
                                  UNIPROTS])
KNOWLEDGE_TYPES_INT = [GOS, SBOS,
                       CHEBIS, KEGG_SPEC,
                       KEGG_PROC, UNIPROTS]
KNOWLEDGE_TYPES_REP = ['go', 'sbo',
                       'chebi', 'kegg_species',
                       'kegg_process', 'uniprot']
KNOWLEDGE_TYPES_ZIP = zip(KNOWLEDGE_TYPES_INT, KNOWLEDGE_TYPES_REP)
KNOWLEDGE_TYPES_DCT = dict()
for ele in KNOWLEDGE_TYPES_ZIP:
  KNOWLEDGE_TYPES_DCT.update(dict.fromkeys(ele[0], ele[1]))

# do we need this at this point? 
ALL_KNOWLEDGE_TERMS = {'go':GOS,
					   'sbo': SBOS,
					   'chebi': CHEBIS,
					   'kegg_species': KEGG_SPEC,
					   'kegg_process': KEGG_PROC,
					   'uniprot': UNIPROTS,
					   }
# items are a set - union of multiple sets
# OBJECT_ONT_MAP_RAW = {MODEL: set.union(*[GOS, SBOS, KEGG_PROC]),
#                       REACTION: set.union(*[GOS, SBOS, KEGG_PROC]),
#                       SPECIES: set.union(*[KEGG_SPEC, UNIPROTS]),
#                       COMPARTMENT: set.union(*[KEGG_SPEC, UNIPROTS]),
#                      }

# physical entity.. and occuring entity.. is from SBO

PROCESS_ROOTS = {'biological_process', 'molecular_function',
                 'kegg_process', 'occurring entity representation'}
# COMPONENT_TERMS = {'cellular_component', 'kegg_species', 'chemical entity',
#                    'uniprot', 'physical entity representation'}
SPECIES_ROOTS = {'cellular_component', 'kegg_species', 'chemical entity',
                   'uniprot', 'physical entity representation'}
COMPARTMENT_ROOTS = {'cellular_component', 'physical entity representation'}            
# when konwledge resources were mapped to KNOWLEDGE_TYPES_REP
OBJECT_ONT_MAP_FILT = {MODEL: PROCESS_ROOTS,
                       REACTION: PROCESS_ROOTS,
                       SPECIES: SPECIES_ROOTS,
                       COMPARTMENT: COMPARTMENT_ROOTS,
                      }


# SBO terms
# categorical parents. Children of 'SBO:0000000'. 
MATH_EXP = 'SBO:0000064'
META_REP = 'SBO:0000544'
MODEL_FRAME = 'SBO:0000004'
ENTITY_REP = 'SBO:0000231'
PART_ROLE = 'SBO:0000003'
PHYSICAL_ENT = 'SBO:0000236'
SYS_PARAM = 'SBO:0000545'

SBO_ROOTS = [MATH_EXP, META_REP,
             MODEL_FRAME, ENTITY_REP,
             PART_ROLE, PHYSICAL_ENT,
             SYS_PARAM]

SBO_ROOT_DICT = {MATH_EXP:'mathematical expression',
                META_REP:'metadata representation',
                MODEL_FRAME:'modelling framework',
                ENTITY_REP:'occurring entity representation',
                PART_ROLE:'participant role',
                PHYSICAL_ENT:'physical entity representation',
                SYS_PARAM:'systems description parameter',
                None: "None"
                }



# CHEBI terms
CHEMICAL_ENTITY = "CHEBI:24431"
CHEBI_ROOTS = [CHEMICAL_ENTITY]
CHEBI_ROOT_DICT = {CHEMICAL_ENTITY: "chemical entity",
                   None: "None"
                   }

# DAG ontologies (GO, SBO, CHEBI)
DAG_ROOT_MAP = {"go":GO_ROOT_DICT,
                "sbo":SBO_ROOT_DICT, 
                "chebi":CHEBI_ROOT_DICT}
























