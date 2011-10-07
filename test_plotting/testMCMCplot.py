
import tmcmc

fileMCMC = 'test1.mcmc'
#fileMCMC = 'MCMC4plot.mcmc'

#print parList

Stats = tmcmc.iopostmcmc.readALLStats(cov='COV.stat',\
        spear='SPEAR.stat',pear='PEAR.stat')

spaceTop = 1.25

#print parList
tmcmc.plotmcmc.trianglePlotTT(fileMCMC,Stats,spaceTop,lowchi='FIT1.par',minuit='FIT2.par')

