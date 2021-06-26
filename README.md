[![Build Status](https://www.travis-ci.com/woosubs/SBMate.svg?token=AZ9nCjqJmNF7xVsjbZBP&branch=main)](https://www.travis-ci.com/woosubs/SBMate)

[![Coverage Status](https://coveralls.io/repos/github/woosubs/SBMate/badge.svg?branch=main)](https://coveralls.io/github/woosubs/SBMate?branch=main)

# SBMate
Systems Biology Model AnnoTation Evaluator

## Overview
``SBMate`` evaluates the quality of annotations in SBML model entities, especially libsbml.Model, libsbml.Species, libsbml.Compartment, and libsbml.Reaction. Currently, it examines annotationos from five knowledge resources, CHEBI, GO, KEGG, SBO, and UNIPROT. 
 
SBMate calculates three metrics: 
1. Coverage checks how many entities of the above four types (model, reaction, species, and compartment) are actually annotated. 
2. Consistency computes how many of such annotated entities has proper annotation. For example, a reaction object should not have a GO cellular component term (GO:0005575 or its children). Consistency identifies such instances and calculates the proprotion of model entities with consistent annotation. 
3. Finally, specificity is a measure of how 'precise' such consistent annotations are. This is obtained by utilizing the hierarchical structures of knowledge resource terms, such as the directed acyclic graphs of SBO and GO. 

More detailed discussions can be found in our manuscript (in preparation). 

## Example
It is quite easy to use SBMate, as there is just one main main method, sbmate.getMetrics().

<img src="https://github.com/woosubs/SBMate/blob/main/png/run_sbmate.png" width="800"/>

By default, SBMate produces a report summarizing the three scores:

<img src="https://github.com/woosubs/SBMate/blob/main/png/result_report.png" width="800"/>

Another option is to create a pandas DataFrame, as below:

<img src="https://github.com/woosubs/SBMate/blob/main/png/run_sbmate_table.png" width="800"/>

And you will get the dataframe. 

<img src="https://github.com/woosubs/SBMate/blob/main/png/result_table.png" width="800"/>
