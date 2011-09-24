
import tmcmc
import numpy as np
import pylab 

# Read data
ObservedData = tmcmc.mcmc.ReadMultiList('lclist.ls')
NuisanceData = tmcmc.mcmc.ReadDetrendFile('NUS.ONOFF.data')

# Read Start and Bound Parameter files
ModelParams = tmcmc.iomcmc.ReadStartParams('START.data')
BoundParams = tmcmc.iomcmc.ReadBoundFile('BOUNDS.TEST.data')

ModelData = tmcmc.myfunc.MTQ_multidepth_tduration(ModelParams,ObservedData)
DetrendedData = tmcmc.mcmc.DetrendData(ObservedData,ModelData,NuisanceData,'',False)

from matplotlib import pyplot as plt

shift = {'T1':0.0e0,'T2':0.02e0,'T3':0.04e0}
#Tmid = {'T1':55494.919,'T2':55591.628966,'T3':55625.63486}
Tmid = {'T1':55494.919,'T2':55591.705,'T3':55625.71}

for TT in DetrendedData.keys():
    if TT.startswith('T'):
        x = np.array(DetrendedData[TT]['x'])
        y = np.array(DetrendedData[TT]['y'])
        yerr = np.array(DetrendedData[TT]['yerr'])
        ymod = ModelData[TT]['y']
        pylab.plot(x-Tmid[TT],y-shift[TT],'bo')
        pylab.errorbar(x-Tmid[TT],y-shift[TT],yerr=yerr,fmt=None)
        pylab.plot(x-Tmid[TT],ymod-shift[TT],'r-')
        chisq = tmcmc.mcmc.chisq(y,yerr,ymod) 
        print chisq, TT, len(y), chisq/len(y)
        ofile = open('testchisq.'+TT+'.data','w')
        for i in range(len(x)):
            print >> ofile,x[i],'|',y[i],'|',yerr[i],'|',ymod[i]
        ofile.close()
        
yall = DetrendedData['all']['y']
modall = ModelData['all']['y']
errall = DetrendedData['all']['yerr']
print tmcmc.mcmc.chisq(yall,errall,modall)


plt.show()
