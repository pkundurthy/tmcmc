import os
import sys
import cPickle as pickle
from tmcmc import DataFuncPrep as dfp
from tmcmc import class_fitprep as cfp

Object = cfp.Object(sys.argv[1])
DataPrepPath = cfp.DataPrepPath

APList = []
TTList = []

for fileName in os.listdir(DataPrepPath):
    if fileName.startswith(Object.name) and fileName.endswith('.data'):
        AP = dfp.getAP(fileName)
        APList.append(AP)
        TT = dfp.getTT(fileName,Object.name)
        TTList.append(TT)

TTList = list(set(TTList))
APList = list(set(APList))

for AP in APList:
    LCListName = DataPrepPath+Object.name+'.LC.AP'+AP+'.list'
    NListName = DataPrepPath+Object.name+'.NUS.AP'+AP+'.onoff'
    LCListObject = open(LCListName,'w')
    NListObject = open(NListName,'w')
    print >> LCListObject, '# FileName | TTag '
    print >> NListObject, '# NUISANCE Data | TTag | '+dfp.detrendHeader.strip('#')
    for TT in TTList:
        print >> LCListObject, DataPrepPath+Object.name+'.AP'+AP+'.'+TT+'.lc'+'|'+TT
        SwitchLine = dfp.getSwitchLine(Object.name,TT)
        #print TT, SwitchLine
        print >> NListObject, DataPrepPath+Object.name+'.AP'+AP+'.'+TT+'.nus'+'|'+TT+SwitchLine
            
    #print 'writing: %s' % (NListName)
    #print '%s' % (LCListName)