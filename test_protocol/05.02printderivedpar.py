
import tmcmc


LowChiFile = 'LOWESTCHISQ.TEST.data'
outLOWCHI = 'derLOWCHISQParams.par'
tmcmc.derived_MTQ_2011.printDerivedParFile_MTQ_2011(LowChiFile,outLOWCHI)

MINUITFile = 'MINUITPARAMS.TEST.data'
outMINUIT = 'derMINUITParams.par'
tmcmc.derived_MTQ_2011.printDerivedParFile_MTQ_2011(MINUITFile,outMINUIT)

CropFile = 'cropDERIVED.TEST.mcmc'
tmcmc.iopostmcmc.printErrors(CropFile,outLOWCHI,'error_derLOWESTCHISQ.TEST.error')
tmcmc.iopostmcmc.printErrors(CropFile,outMINUIT,'error_derMINUIT.TEST.error')

