import os
import sys
import cPickle as pickle
import tmcmc
from tmcmc import DataFuncPrep as dfp
from tmcmc import class_fitprep as cfp
import pylab as plt
import numpy as np

Object = cfp.Object('WASP2')
Object.InitiateCase('MINUIT.FIRSTTRY')

DataPrepPath = cfp.DataPrepPath
FigurePath = cfp.FigurePath

OptAp = pickle.load(open(cfp.PicklePath+Object.name+'.OptAp.pickle','rb'))

exec("from tmcmc.myfunc import %s as ModelFunc" % (Object.FuncName))
ModelParams = tmcmc.iomcmc.ReadStartParams(DataPrepPath+'GUESS.'+Object.name+'.par')

for fileName in os.listdir(DataPrepPath):
    if fileName.startswith(Object.name) and \
       fileName.endswith('.nus'):
        name_split = map(str, fileName.split('.'))
        AP = name_split[1].strip('AP')
        TT = name_split[2]
        if TT in ['T8','T9','T10']:
            lcfile = Object.name+'.AP'+AP+'.'+TT+'.lc'
            nusfile = Object.name+'.AP'+AP+'.'+TT+'.nus'
            #os.system('wc %s' % DataPrepPath+nusfile )
            #os.system('wc %s' % DataPrepPath+lcfile )
            dt_data = dfp.readNusFile(DataPrepPath+nusfile)
            lc_data = tmcmc.iomcmc.ReadSingleDataFile(DataPrepPath+lcfile)
            time = np.array(lc_data['all']['x'])
            diffT = 45e0/86400e0
            if len(time) > 0:
                #print dt_data.keys()
                T0 = time[0]
                new_index = (time-T0)//diffT
                dt_data['index'] = new_index
                dfp.writeUpdatedNuisance(DataPrepPath+nusfile, dt_data)

#sys.exit()
## OPT AP X
#LCListName = DataPrepPath+Object.name+'.LC.listx'
#NListName = DataPrepPath+Object.name+'.NUS.onoffx'
#ObservedData = tmcmc.iomcmc.ReadMultiList(LCListName)
#NuisanceData = tmcmc.iomcmc.ReadDetrendFile(NListName)
#ModelData = ModelFunc(ModelParams,ObservedData)
#HiResData = dfp.HiRes(ObservedData,5000)
#HiResModel = ModelFunc(ModelParams,HiResData)
#DetrendedData = tmcmc.mcmc.DetrendData(ObservedData,ModelData,NuisanceData,'',False)

#print NuisanceData['T9']['dtparams']['index']['used']
