import tmcmc

CropFile = 'cropMCMC.TEST.mcmc'
#CropFile = 'testCrop1000.mcmc'

# auto-correlation & statistics
lowtol = 0.01
jmax = 1500
makePlotsFlag = True
tmcmc.postmcmc.autocorMCMC(CropFile,lowtol,jmax,'OutputStats.TEST.data',makePlotsFlag,Silent=False,ftag='TEST.')

#covariance statistics
tmcmc.postmcmc.covcorStats(CropFile,'TEST.')