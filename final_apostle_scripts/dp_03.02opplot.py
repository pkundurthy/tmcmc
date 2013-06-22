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

OptAp = pickle.load(open(cfp.PicklePath+Object.name+'.OptAp.pickle','rb'))

exec("from tmcmc.myfunc import %s as ModelFunc" % (Object.FuncName))
ModelParams = tmcmc.iomcmc.ReadStartParams(DataPrepPath+'GUESS.'+Object.name+'.par')

LCListName = DataPrepPath+Object.name+'.LC.listx'
NListName = DataPrepPath+Object.name+'.NUS.onoffx'
ObservedData = tmcmc.iomcmc.ReadMultiList(LCListName)
NuisanceData = tmcmc.iomcmc.ReadDetrendFile(NListName)
ModelData = ModelFunc(ModelParams,ObservedData)
HiResData = dfp.HiRes(ObservedData,5000)
HiResModel = ModelFunc(ModelParams,HiResData)
DetrendedData = tmcmc.mcmc.DetrendData(ObservedData,ModelData,NuisanceData,'',False)

#for TT in DetrendedData.keys():
    #print TT, DetrendedData[TT]['x']

#sys.exit()

ChiSQ, DetrendedData = dfp.chisq(DetrendedData,ModelData)
#print DetrendedData['T1']['x']
DOF = len(DetrendedData['all']['y'])-dfp.NOpen(ModelParams)
print ChiSQ, DOF, ChiSQ/DOF
OtherInfo = {}

ScaleTT = {}
#scaling individual nights
for TT in ObservedData.keys():
    if TT.startswith('T'):
        med_err = np.median(DetrendedData[TT]['yerr'])
        scale = OptAp[TT]['min_rms']/med_err
        DetrendedData[TT]['yerr'] = np.array(DetrendedData[TT]['yerr'])*scale
        ObservedData[TT]['yerr'] = np.array(ObservedData[TT]['yerr'])*scale
        ScaleTT[TT] = scale

ChiSQ, DetrendedData = dfp.chisq(DetrendedData,ModelData)
DOF = len(DetrendedData['all']['y'])-dfp.NOpen(ModelParams)
scale2 = np.sqrt(ChiSQ/DOF)
#print ChiSQ, DOF, scale2

for TT in ObservedData.keys():
    if TT.startswith('T'):
        DetrendedData[TT]['yerr'] = np.array(DetrendedData[TT]['yerr'])*scale2
        ObservedData[TT]['yerr'] = np.array(ObservedData[TT]['yerr'])*scale2 
        #ScaleTT[TT] = ScaleTT[TT]*scale2
        med_err = np.median(DetrendedData[TT]['yerr'])
        yobs = DetrendedData[TT]['y']
        yerr = DetrendedData[TT]['yerr']
        ymod = ModelData[TT]['y']
        ChiSQ1 = tmcmc.mcmc.chisq(yobs,yerr,ymod)
        DOF1 = len(DetrendedData['all']['y'])-dfp.NOpen(ModelParams)+dfp.NTTs(ModelParams)-1
        #print TT, OptAp[TT]['ap'], OptAp[TT]['min_rms']*1e6, ChiSQ1/DOF1
        OtherInfo[TT] = {'err_scale':ScaleTT[TT]*scale2,'med_err':med_err}
        time = np.array(DetrendedData[TT]['x'])-ModelParams['T0.'+TT]['value']
        timeHiRes = np.array(HiResData[TT]['x'])-ModelParams['T0.'+TT]['value']
        plt.plot(time,DetrendedData[TT]['y'],'b.')
        plt.plot(timeHiRes,HiResModel[TT]['y'],'r-')
        plt.errorbar(time,DetrendedData[TT]['y'],yerr=DetrendedData[TT]['yerr'],fmt=None)
        plt.xlabel('Time - Mid Transit Time (days)')
        plt.ylabel('Normalized Flux Ratio')
        plt.title(Object.name+' '+TT+' '+cfp.DateStrings[Object.name][TT])
        plt.savefig(FigurePath+'LCTestPlot.'+Object.name+'.'+TT+'.png')
        plt.clf()
        
        # ------------------------------- #
        out_lcfile = DataPrepPath+Object.name+'.'+TT+'.lcx'
        dfp.writeLCFile(ObservedData[TT],out_lcfile)
        

ChiSQ, DetrendedData = dfp.chisq(DetrendedData,ModelData)
DOF = len(DetrendedData['all']['y'])-dfp.NOpen(ModelParams)
OtherInfo['all'] = {'ChiSQ':ChiSQ,'DOF':DOF}

fileOut = open(cfp.PicklePath+Object.name+'.PhotInfo.pickle','wb')
pickle.dump(OtherInfo,fileOut,-1)
fileOut.close()
print ChiSQ, DOF, ChiSQ/DOF
