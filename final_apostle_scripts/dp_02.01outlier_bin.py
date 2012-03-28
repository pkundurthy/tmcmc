import os
import sys
import cPickle as pickle
import tmcmc
from tmcmc import DataFuncPrep as dfp
from tmcmc import class_fitprep as cfp
import numpy as np

Object = cfp.Object(sys.argv[1])
Object.InitiateCase('MINUIT.FIRSTTRY')

DataPrepPath = cfp.DataPrepPath

exec("from tmcmc.myfunc import %s as ModelFunc" % (Object.FuncName))
ModelParams = tmcmc.iomcmc.ReadStartParams(DataPrepPath+'GUESS.'+Object.name+'.par')

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

#FracRej = pickle.load(open(cfp.PicklePath+Object.name+'.FracRej.pickle','rb'))

if Object.name == 'WASP2' or Object.name == 'XO2':
    bcase = float(sys.argv[2])
    APList = []
    if Object.name == 'WASP2':
        SplitNum = 7e0
    else:
        SplitNum = 4e0
    for i in np.arange(SplitNum):
        ApNum = (bcase-1)*SplitNum + (i+1)
        if ApNum < 50e0:
            ApStr = format(ApNum, '.0f')
            APList.append(ApStr)
    
for AP in APList:
    LCListName = DataPrepPath+Object.name+'.LC.AP'+AP+'.list0'
    NListName = DataPrepPath+Object.name+'.NUS.AP'+AP+'.onoff0'

    ObservedData = tmcmc.iomcmc.ReadMultiList(LCListName)
    NuisanceData = tmcmc.iomcmc.ReadDetrendFile(NListName)
    ModelData = ModelFunc(ModelParams,ObservedData)
    DetrendedData = tmcmc.mcmc.DetrendData(ObservedData,ModelData,NuisanceData,'',False)
    goodids, badids = dfp.rejectOutliers(DetrendedData,ModelData,5.0e0)

    FracRejFile =  open(cfp.PicklePath+Object.name+'.FracRej.'+AP+'.notes','w')
    
    NewNuisanceData = dfp.mkNuisance(NuisanceData)
    for TT in DetrendedData.keys():
        if TT.startswith('T'):
            bad = len(badids[TT])
            n_all = len(badids[TT])+len(goodids[TT])
            if n_all != 0:
                fRej = float(bad)/float(n_all)
            else:
                fRej = float('nan')

            print >> FracRejFile, AP+' | '+TT+' | '+str(fRej)
            #print ObservedData.keys(), NewNuisanceData.keys(), goodids.keys()
            outdata = dfp.applyGoodIDs(ObservedData[TT],NewNuisanceData[TT],goodids[TT])
            if dfp.ToBeBinned(Object.name,TT):
                outdata = dfp.BinnedData(outdata,45e0)
            NuisFile = DataPrepPath+Object.name+'.AP'+AP+'.'+TT+'.nus'
            LCFile = DataPrepPath+Object.name+'.AP'+AP+'.'+TT+'.lc'
            NuisFileObject = open(NuisFile,'w')
            LCFileObject = open(LCFile,'w')
        
            dtheader = dfp.detrendHeader
            LCheader = dfp.LCHeader
            print >> NuisFileObject, dtheader
            print >> LCFileObject, LCheader
            for i in range(len(outdata['time'])):
                lcline = dfp.LClineFromIndex(outdata,i)
                dtline = dfp.dtlineFromIndex(outdata,i)
                print >> NuisFileObject, dtline 
                print >> LCFileObject, lcline

            print 'outlier/binning writing: %s' % (NuisFile)
            print '%s' % (LCFile)

FracRejFile.close()