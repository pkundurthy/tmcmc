import os
import sys
import cPickle as pickle
import tmcmc
from tmcmc import DataFuncPrep as dfp
from tmcmc import class_fitprep as cfp
import pylab as plt
import numpy as np

#NUISANCE Data   | T# | airmass | x1 | y1 | x2 | y2 | msky1 | msky2 | gsky | a0 | sD1 | sD2 | sF1 | sF2 | telfocus | telrot | time | diff_sky | dist | sky_ratio1 | sky_ratio2

Object = cfp.Object(sys.argv[1])
Object.InitiateCase('MINUIT.FIRSTTRY')

DataPrepPath = cfp.DataPrepPath
FigurePath = cfp.FigurePath

exec("from tmcmc.myfunc import %s as ModelFunc" % (Object.FuncName))
ModelParams = tmcmc.mcmc.ReadStartParams(DataPrepPath+'GUESS.'+Object.name+'.par')

LCListName = DataPrepPath+Object.name+'.LC.listx1'
NListName = DataPrepPath+Object.name+'.NUS.onoffx1'

ObservedData = tmcmc.mcmc.ReadMultiList(LCListName)
NuisanceData = tmcmc.mcmc.ReadDetrendFile(NListName)

#for TT in ['T8','T9','T10']:
    #print dfp.getOpenNusPars(NuisanceData,TT)
    
#sys.exit()

for TT in NuisanceData.keys():
    Line = TT
    if TT.startswith('T'):
        for dtpar in NuisanceData[TT]['dtparams'].keys():
        #for dtpar in dfp.getOpenNusPars(NuisanceData,TT):
            boolTrue = NuisanceData[TT]['dtparams'][dtpar]['used']
            Ndata = len(NuisanceData[TT]['dtparams'][dtpar]['data'])
            if Ndata != 0: 
                maxd = max(NuisanceData[TT]['dtparams'][dtpar]['data'])
            else:
                maxd = 'None'
            
            #print dtpar, Ndata, maxd, TT
            #Line += '| ('+dtpar+'='+str(boolTrue)+','+str(Ndata)+')'
            #if TT == 'T9': print TT, dtpar, boolTrue, Ndata
    #print Line

#sys.exit()

# WASP2 T1 ['gsky','dist','diff_sky','airmass'] ON
# WASP2 T2 ['airmass','dist','sky_ratio1','diff_sky'] ON
# WASP2 T3 ['airmass','dist','a0','diff_sky'] ON
# WASP2 T4 ['airmass','dist','a0','diff_sky'] ON
# WASP2 T5 ['airmass','dist','a0','diff_sky'] ON
# WASP2 T6 ['airmass','dist','a0','diff_sky'] ON
# WASP2 T7 ['airmass','dist','a0','diff_sky'] ON

# WASP2 T8 ['airmass','dist','sky_ratio2',\
#           'sky_ratio1','diff_sky','sF1','gsky','y1','x1','sD1'] ON


#sys.exit()
OffList = []
TT = 'T9'
All = ['telfocus','telrot','a0']
O1 = ['x1','y1','sD1','sF1','msky1','sky_ratio1']
O2 = ['x2','y2','sD2','sF2','msky2','sky_ratio2']
NN = ['gsky','dist','diff_sky','airmass','index']

OffList.extend(All)
OffList.extend(O1)
OffList.extend(O2)
#OffList.extend(NN)
#OffList.remove(['sD1','sF1'])
#for par in ['msky1','sky_ratio1']: OffList.remove(par)
#OffList.extend(['a0','sF2','x2','sD2','msky2','msky1'])
#OffList.extend(['a0','sF1','sD1','y1','x1','msky1','sky_ratio1','dist','diff_sky','gsky'])
#OffList.remove('telrot')
#OffList.remove('dist')
#OffList.remove('diff_sky')
#OffList.remove('index')

for dtpar in NuisanceData[TT]['dtparams'].keys():
    Ndata = len(NuisanceData[TT]['dtparams'][dtpar]['data'])
    used = NuisanceData[TT]['dtparams'][dtpar]['used']
    #print dtpar, used , Ndata
     
#sys.exit()
NuisanceData, OnList = dfp.SwitchOFF(NuisanceData,OffList,[TT])

ModelData = ModelFunc(ModelParams,ObservedData)
HiResData = dfp.HiRes(ObservedData,5000)
HiResModel = ModelFunc(ModelParams,HiResData)

DetrendedData = tmcmc.mcmc.DetrendData(ObservedData,ModelData,NuisanceData,'',False)

#print DetrendedData[TT]['dtcoeff'].keys()
#print OffList
#print OnList

for dtparkey in OnList:
    coeff = DetrendedData[TT]['dtcoeff'][dtparkey]['coeff']
    maxd = DetrendedData[TT]['dtcoeff'][dtparkey]['maxd']
    coerr = DetrendedData[TT]['dtcoeff'][dtparkey]['coerr']
    errDT = format(np.sqrt((maxd**2)*coerr),'0.6f')
    errOD = format(np.max(ObservedData[TT]['yerr']),'0.6f')
    print errDT, errOD, coeff*maxd, dtparkey 

x = np.array(ObservedData[TT]['x']) - ModelParams['T0.'+TT]['value']
yobs = np.array(ObservedData[TT]['y'])
y = np.array(DetrendedData[TT]['y'])
yerr = np.array(DetrendedData[TT]['yerr'])
ymod = np.array(ModelData[TT]['y'])
    
#plt.plot(x,y/ymod,'b.')
#plt.plot(x,y,'b.')
#plt.plot(x,yobs,'r.')
#plt.plot(x,ymod,'g-')
#plt.errorbar(x,y,yerr=yerr,fmt=None)
#plt.title(Object.name+' '+TT)
#plt.show()
#plt.savefig(cfp.FigurePath+'dtTEST.'+Object.name+'.'+TT+'.png')
#plt.clf()

for dtpar in NuisanceData[TT]['dtparams'].keys():
    #if NuisanceData[TT]['dtparams'][dtpar]['used']:
    if True:
        x = np.array(DetrendedData[TT]['x']) - ModelParams['T0.'+TT]['value']
        plt.plot(x,NuisanceData[TT]['dtparams'][dtpar]['data'],'b.')
        plt.title(TT+' '+dtpar)
        plt.show()

#print dtparlist
#maxList = []
#parList = []
#spTT = 'T1'
#for TT in NuisanceData.keys():
    #if TT.startswith('T'):
        #dtparlist = DetrendedData[TT]['dtcoeff'].keys()
        #for dtparkey in sorted(dtparlist):
            #if dtparkey != 'const':
                #if NuisanceData[TT]['dtparams'][dtparkey]['used']:
                    #coeff = DetrendedData[TT]['dtcoeff'][dtparkey]['coeff']
                    #maxd = DetrendedData[TT]['dtcoeff'][dtparkey]['maxd']
                    #coerr = DetrendedData[TT]['dtcoeff'][dtparkey]['coerr']
                    #if TT == spTT:
                        #parList.append(dtparkey)
                        #maxList.append((maxd**2)*coerr)
                        #print TT, dtparkey, ((maxd**2)*coerr)**(0.5), max(ObservedData[TT]['yerr'])

#print max(maxList), parList[np.array(maxList).argmax()]

#for dtpar in dfp.detrendPars:
    #for TT in NuisanceData.keys():
        #if TT.startswith('T'):
            #boolTrue = NuisanceData[TT]['dtparams'][dtpar]['used']
            #Ndata = len(NuisanceData[TT]['dtparams'][dtpar]['data'])
            #if TT == spTT: print boolTrue, TT, dtpar, Ndata
            
#OffList = ['sD2','sF2','x2','y2','sky_ratio2','msky1','msky2','telfocus','telrot','a0']
#TTagList = ['T8','T9','T10']
#NuisanceData = dfp.SwitchOFF(NuisanceData,OffList,TTagList)

#for par in OffList:
    #print par, NuisanceData['T1']['dtparams'][par]['used']
