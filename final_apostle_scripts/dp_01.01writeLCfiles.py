import os
import sys
import tmcmc
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
        TT = dfp.getTT(fileName,Object.name)
        APList.append(AP)
        TTList.append(TT)
        
APPs = list(set(APList))
TTs = list(set(TTList))
FluxNorm = {}

for AP in APPs:
    FluxNorm[AP] = {}
    for TT in TTs:
        FluxNorm[AP][TT] = 0

for fileName in os.listdir(DataPrepPath):
    if fileName.startswith(Object.name) and fileName.endswith('.data'):
        AP = dfp.getAP(fileName)
        outdict = dfp.readDataFile(DataPrepPath+fileName)
        TT = dfp.getTT(fileName,Object.name)
        T0 = Object.ParDict['T0.'+TT]['value']
        tT = Object.ParDict['tT']['value']
        tG = Object.ParDict['tG']['value']
        outdict, normalizing_factor = dfp.normalizeFluxRatio(outdict,T0,tT,tG)
        FluxNorm[AP][TT] = normalizing_factor
        NuisFile = DataPrepPath+Object.name+'.AP'+AP+'.'+TT+'.nus0'
        LCFile = DataPrepPath+Object.name+'.AP'+AP+'.'+TT+'.lc0'
        NuisFileObject = open(NuisFile,'w')
        LCFileObject = open(LCFile,'w')
        dtheader = dfp.detrendHeader
        LCheader = dfp.LCHeader
        print >> NuisFileObject, dtheader
        print >> LCFileObject, LCheader
        for i in range(len(outdict['time'])):
            lcline = dfp.LClineFromIndex(outdict,i)
            dtline = dfp.dtlineFromIndex(outdict,i)
            print >> NuisFileObject, dtline 
            print >> LCFileObject, lcline

        print 'writing: %s' % (NuisFile)
        print '%s' % (LCFile)
 
fileOut = open(cfp.PicklePath+Object.name+'.FluxNorm.pickle','wb')
pickle.dump(FluxNorm,fileOut,-1)
fileOut.close()