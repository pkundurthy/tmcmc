import os
import sys
import cPickle as pickle
import tmcmc
from tmcmc import DataFuncPrep as dfp
from tmcmc import class_fitprep as cfp
import pylab as plt
import numpy as np

Object = cfp.Object(sys.argv[1])
Object.InitiateCase('MINUIT.FIRSTTRY')

DataPrepPath = cfp.DataPrepPath
FigurePath = cfp.FigurePath

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
APList2 = APList

rms = {}
goodid_db = {}
bad_err = {}
Completeness = {}

print 'Outlier rejection '
for AP in APList:
    Completeness[AP] = {}
    LCListName = DataPrepPath+Object.name+'.LC.AP'+AP+'.list'
    NListName = DataPrepPath+Object.name+'.NUS.AP'+AP+'.onoff'
    
    ObservedData = tmcmc.iomcmc.ReadMultiList(LCListName)
    NuisanceData = tmcmc.iomcmc.ReadDetrendFile(NListName)
    ModelData = ModelFunc(ModelParams,ObservedData)
    
    HiResData = dfp.HiRes(ObservedData,5000)
    HiResModel = ModelFunc(ModelParams,HiResData)
    
    DetrendedData = tmcmc.mcmc.DetrendData(ObservedData,ModelData,NuisanceData,'',False)
    
    for TT in TTList:
        if TT.startswith('T'):
            if len(DetrendedData[TT]['y']) > 0:
                goodids, badids, bad_err0 = \
                dfp.SecondRejectOutliers(DetrendedData[TT],ModelData[TT],5.0e0, TT)
                Nused = float(len(goodids))
                Nin = float(len(DetrendedData[TT]['y']))
                Completeness[AP][TT] = {'nused':float(Nused),\
                                        'nin':float(Nin)}
                #print TT, AP, Nused, Nin
            else:
                Completeness[AP][TT] = {'nused':0,'nin':0}
            
maxNused = {}
for TT in TTList:
    NList = []
    for AP in APList:
        NList.append(Completeness[AP][TT]['nin'])

    NList = np.array(NList)
    maxNused[TT] = np.max(NList)
    #print np.max(NList), TT, APList[NList.argmax()]

print 'Optimal aperture selection '
for AP in APList:
    bad_err[AP] = {}
    goodid_db[AP] = {}
    rms[AP] = {}
    LCListName = DataPrepPath+Object.name+'.LC.AP'+AP+'.list'
    NListName = DataPrepPath+Object.name+'.NUS.AP'+AP+'.onoff'
    
    ObservedData = tmcmc.iomcmc.ReadMultiList(LCListName)
    NuisanceData = tmcmc.iomcmc.ReadDetrendFile(NListName)
    ModelData = ModelFunc(ModelParams,ObservedData)
    HiResData = dfp.HiRes(ObservedData,5000)
    HiResModel = ModelFunc(ModelParams,HiResData)
    
    DetrendedData = tmcmc.mcmc.DetrendData(ObservedData,ModelData,NuisanceData,'',False)

    for TT in DetrendedData.keys():
        if TT.startswith('T'):
            numUsed = Completeness[AP][TT]['nused']
            numMax = maxNused[TT]
            Completeness[AP][TT]['nmax'] = maxNused[TT]
            if float(numMax) > 0:
                ComNumber = 100e0*numUsed/numMax
            else:
                ComNumber = -99
            
            if  ComNumber > 50e0:
                goodids, badids, bad_err0 = \
                dfp.SecondRejectOutliers(DetrendedData[TT],ModelData[TT],5.0e0,TT)
                scatter = np.array(DetrendedData[TT]['y']) - np.array(ModelData[TT]['y'])
                rms[AP][TT] = np.std(scatter[goodids])
                goodid_db[AP][TT] = goodids 
                bad_err[AP][TT] = bad_err0
                print TT, 'AP'+str(AP), ComNumber, str(numUsed)+'/'+str(numMax), rms[AP][TT]
            else:
                rms[AP][TT] = float('inf')
                print TT, 'AP'+str(AP), ComNumber, str(numUsed)+'/'+str(numMax), rms[AP][TT]

OptAp = {}

for TT in TTList:
    ap_list, rms_list = dfp.get_optap(rms,TT)
    #print TT, ap_list, rms_list
    minAP = ap_list[rms_list.argmin()]
    minRMS = min(rms_list)
    APstr = str(int(minAP))
    numMax = float(Completeness[APstr][TT]['nmax'])
    numUsed = float(Completeness[APstr][TT]['nused'])
    #print TT, float(Completeness[AP][TT]['nused']), float(maxNum[TT])
    if float(numMax) > 0:
        ComNumber = 100e0*numUsed/numMax
    else:
        ComNumber = -99

    LCListName = DataPrepPath+Object.name+'.LC.AP'+APstr+'.list'
    NListName = DataPrepPath+Object.name+'.NUS.AP'+APstr+'.onoff'
    ObservedData = tmcmc.iomcmc.ReadMultiList(LCListName)
    NuisanceData = tmcmc.iomcmc.ReadDetrendFile(NListName)
    
    lcfile = DataPrepPath+Object.name+'.AP'+APstr+'.'+TT+'.lc'
    nusfile = DataPrepPath+Object.name+'.AP'+APstr+'.'+TT+'.nus'
    
    out_lcfile = DataPrepPath+Object.name+'.'+TT+'.lcx'
    out_nusfile = DataPrepPath+Object.name+'.'+TT+'.nusx'
    #Figure
    plt.plot(ap_list,rms_list*1e6,'b.')
    plt.axvline(x=minAP, ymin=0, ymax=1)
    #print ap_list, rms_list, AP
    plt.yscale('log')
    plt.ylim([1e2,1e4])
    plt.xlabel('Aperture Radius (pix)')
    plt.ylabel('rms (ppm)')
    plt.title(Object.name+' '+TT+' '+cfp.DateStrings[Object.name][TT])
    plt.savefig(FigurePath+Object.name+'.optAp.'+TT+'.png')
    plt.clf()
    
    OptAp[TT] = {'ap':minAP,'min_rms':minRMS,\
                 'lcfile':lcfile,'nusfile':nusfile,\
                 'out_lcfile':out_lcfile,'out_nusfile':out_nusfile}
    
    LC_IN_LIST = open(lcfile,'r').readlines()
    NUS_IN_LIST = open(nusfile,'r').readlines()
    LC_IN_LIST = LC_IN_LIST[1:] 
    NUS_IN_LIST = NUS_IN_LIST[1:]
    
    LC_OUT_FILE = open(out_lcfile,'w')
    NUS_OUT_FILE = open(out_nusfile,'w')

    print >> LC_OUT_FILE, dfp.LCHeader
    print >> NUS_OUT_FILE, dfp.detrendHeader
    for iLine in range(len(LC_IN_LIST)):
        lcline = LC_IN_LIST[iLine].strip('\n')
        nusline = NUS_IN_LIST[iLine].strip('\n')
        if iLine in goodid_db[APstr][TT]:
            print >> LC_OUT_FILE, lcline
            print >> NUS_OUT_FILE, nusline

fileOut = open(cfp.PicklePath+Object.name+'.OptAp.pickle','wb')
pickle.dump(OptAp,fileOut,-1)
fileOut.close()

LCListName = DataPrepPath+Object.name+'.LC.listx'
NListName = DataPrepPath+Object.name+'.NUS.onoffx'

LCListObject = open(LCListName,'w')
NListObject = open(NListName,'w')
print >> LCListObject, '# FileName | TTag '
print >> NListObject, '# NUISANCE Data | TTag | '+dfp.detrendHeader.strip('#')
for TT in TTList:
    print >> LCListObject,OptAp[TT]['out_lcfile']+'|'+TT
    SwitchLine = dfp.getSwitchLine(Object.name,TT)
    #print Object.name, TT, SwitchLine
    print >> NListObject, OptAp[TT]['out_nusfile']+'|'+TT+SwitchLine

print 'writing: %s' % (NListName)
print '%s' % (LCListName)

LCListName1 = DataPrepPath+Object.name+'.LC.listx1'
NListName1 = DataPrepPath+Object.name+'.NUS.onoffx1'

LCListObject1 = open(LCListName1,'w')
NListObject1 = open(NListName1,'w')
print >> LCListObject1, '# FileName | TTag '
print >> NListObject1, '# NUISANCE Data | TTag | '+dfp.detrendHeader.strip('#')
for TT in TTList:
    ap_list, rms_list = dfp.get_optap(rms,TT)
    minAP = ap_list[rms_list.argmin()]
    minRMS = min(rms_list)
    APstr = str(int(minAP))
    lcfile = DataPrepPath+Object.name+'.AP'+APstr+'.'+TT+'.lc'
    nusfile = DataPrepPath+Object.name+'.AP'+APstr+'.'+TT+'.nus'
    
    print >> LCListObject1, lcfile+'|'+TT
    SwitchLine = dfp.getSwitchLine(Object.name,TT,supress=True)
    #print Object.name, TT, SwitchLine
    print >> NListObject1, nusfile+'|'+TT+SwitchLine

print 'writing: %s' % (NListName1)
print '%s' % (LCListName1)
