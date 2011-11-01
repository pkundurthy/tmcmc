import tmcmc
import pylab

x = tmcmc.iopostmcmc.correctionFromDTfile('DTCOEFF.MCMC.TEST.mcmc','NUS.ONOFF.data')

ObservedData = tmcmc.mcmc.ReadMultiList('lclist.ls')
ModelParams = tmcmc.iomcmc.ReadStartParams('STARTPARAMS.TEST.data')
FuncName = 'MTQ_multidepth_tduration'
NuisanceData = tmcmc.mcmc.ReadDetrendFile('NUS.ONOFF.data')

y = tmcmc.iopostmcmc.correctionFromMCMC('MCMC.TEST.mcmc',\
    ObservedData,ModelParams,NuisanceData,FuncName)

print y[1]['T1']
dtmax = []
for num in x.keys():
    for tag in x[num].keys():
        dtmax.append( max( abs(x[num][tag] - y[num][tag]) ) )
        #pylab.plot(abs(x[num][tag] - y[num][tag]),'b.')

pylab.plot(dtmax,'b.')
print max(dtmax)
pylab.show()