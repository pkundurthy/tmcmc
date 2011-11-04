
import tmcmc
import os
import pylab

#Read data
ObservedData = tmcmc.mcmc.ReadMultiList('lclist.ls')
NuisanceData = tmcmc.mcmc.ReadDetrendFile('NUS.ONOFF.data')
os.system('rm -v DTCOEFF*')

# Read Start and Bound Parameter files
ModelParams = tmcmc.iomcmc.ReadStartParams('STARTPARAMS.TEST.data')
BoundParams = tmcmc.iomcmc.ReadBoundFile('BOUNDS.TEST.data')

##SHIFT starting point
#ShiftFactor = 15e0
##ShiftFactor = -15e0
for Param in ModelParams.keys():
    if ModelParams[Param]['open']:
        ModelParams[Param]['step'] *= 0.01
        
Nsteps = 5000
func = 'MTQ_multidepth_tduration'
DerivedFunctionName = 'returnDerivedLine_MTQ2011'

OutFile = 'MCMC.TEST.mcmc'
DerivedFile0 = 'DERIVED_during.TEST.mcmc'

tmcmc.mcmc.mcmc_mh_adapt_derived(Nsteps,func,ObservedData,\
    ModelParams,NuisanceData,BoundParams,True,False,True,\
    OutFile,DerivedFunctionName,DerivedFile0,True)

os.system('mv DTCOEFF.MCMC.TEST.mcmc DTCOEFF_during.MCMC.TEST.mcmc')

STARTFILE = 'STARTPARAMS.TEST.data'           # input
MCMCfile = 'MCMC.TEST.mcmc'                   # input
DerivedFile = 'DERIVED_after.TEST.mcmc'       # output
tmcmc.myderivedfunc.printDerived_MTQ_2011(STARTFILE,MCMCfile,DerivedFile)

statement = "mv -v %s temp" % DerivedFile0 
os.system(statement)
statement = "head -1 %s > %s" % (DerivedFile, DerivedFile0) 
os.system(statement)
statement = "cat temp >> %s" % DerivedFile0
os.system(statement)

#Corr1 = tmcmc.iopostmcmc.correctionFromDTfile('DTCOEFF_during.MCMC.TEST.mcmc','NUS.ONOFF.data')
#Corr2 = tmcmc.iopostmcmc.correctionFromMCMC('MCMC.TEST.mcmc',ObservedData,ModelParams,NuisanceData,FuncName)

#dtmax = []
#for num in Corr1.keys():
    #for tag in Corr1[num].keys():
        #dtmax.append( max( abs(Corr1[num][tag] - Corr2[num][tag]) ) )

#pylab.plot(dtmax,'b.')
#pylab.show()

#Der1 = tmcmc.iopostmcmc.readMCMC('DERIVED_before.TEST.mcmc')
#Der2 = tmcmc.iopostmcmc.readMCMC('DERIVED_after.TEST.mcmc')

#DtDer
#for key in Der1.keys():
    #if not tmcmc.iopostmcmc.isNonParam(key):
        #DtDer.append(max( abs(Der1[key]-Der2[key])))

#pylab.plot(DtDer,'b.')
#pylab.show()

