import tmcmc

CropFile = 'cropMCMC.TEST.mcmc'
#CropFile = 'testCrop1000.mcmc'

# get lowest chisq
ModelParams = tmcmc.iomcmc.ReadStartParams('STARTPARAMS.TEST.data')
tmcmc.iomcmc.WriteLowestChisq(CropFile,ModelParams,'LOWESTCHISQ.TEST.data',True)

tmcmc.iopostmcmc.printErrors(CropFile,'LOWESTCHISQ.TEST.data','errorsLOWESTCHISQ.TEST.data')
