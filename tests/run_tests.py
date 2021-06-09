# run_tests.py
# run all tests within 
# the tests folder

import os
import sys
sys.path.append(os.path.join(os.getcwd(), '../'))

from SBMate import constants as cn

print("Success!")
print(cn.BIOMODEL_OBJECTS)