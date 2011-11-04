import tmcmc
import pylab
import numpy as np

FuncName = 'MTQ_multidepth_tduration'

ObservedData = tmcmc.mcmc.ReadMultiList('lclist.ls')
NuisanceData = tmcmc.mcmc.ReadDetrendFile('NUS.ONOFF.data')
ModelParams = tmcmc.iomcmc.ReadStartParams('STARTPARAMS.TEST.data')
BoundParams = tmcmc.iomcmc.ReadBoundFile('BOUNDS.TEST.data')

Corr1 = tmcmc.iopostmcmc.correctionFromDTfile('DTCOEFF_during.MCMC.TEST.mcmc','NUS.ONOFF.data')
Corr2 = tmcmc.iopostmcmc.correctionFromMCMC('MCMC.TEST.mcmc',ObservedData,ModelParams,NuisanceData,FuncName)

dtmax = []
for num in Corr1.keys():
    for tag in Corr1[num].keys():
        print num, tag
        dtmax.append( max( abs(Corr1[num][tag] - Corr2[num][tag]) ) )

pylab.plot(np.array(dtmax)/1e-6,'b.')
pylab.ylabel('Correction Diff (in flux ratio ppm)')
pylab.ylabel('Max(Diff) for NStep(MCMC) x NTransits')
##pylab.show()
pylab.savefig('dtCorrecDiff.png')
pylab.close()

Der1 = tmcmc.iopostmcmc.readMCMC('DERIVED_during.TEST.mcmc')
Der2 = tmcmc.iopostmcmc.readMCMC('DERIVED_after.TEST.mcmc')

DtDer = []
Std1 = []
Std2 = []
par= []
for key in Der1.keys():
    if not tmcmc.iopostmcmc.isNonParam(key):
        arr1 = np.array(Der1[key])
        arr2 = np.array(Der2[key])
        DtDer.append(max( abs(arr1-arr2) ) )
        Std1.append(np.std(arr1))
        Std2.append(np.std(arr2))
        par.append(key)
        
Std1 = np.array(Std1)
Std2 = np.array(Std2)

pylab.plot(DtDer/Std1,'bo')
pylab.plot(DtDer/Std2,'ro')
for key in par:
    idx = par.index(key)
    print idx, len(Std1)
    pylab.text(idx,DtDer[idx]/Std1[idx],key.strip('_'))
pylab.ylabel('Diff / Stdev (parameter)')
pylab.xlabel('Parameter Number')
pylab.savefig('DerDiff.png')
#pylab.show()