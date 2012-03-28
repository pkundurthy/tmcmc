import os
import sys
from tmcmc import DataFuncPrep as dfp
from tmcmc import class_fitprep as cfp

Object = cfp.Object(sys.argv[1])

DataPrepPath = cfp.DataPrepPath

for fileName in os.listdir(DataPrepPath):
    if fileName.startswith(Object.name) and fileName.endswith('x'):
        #print 'cp -v %s %s' % (DataPrepPath+fileName,Object.dataPath)
        os.system('cp -v %s %s' % (DataPrepPath+fileName,Object.dataPath) )