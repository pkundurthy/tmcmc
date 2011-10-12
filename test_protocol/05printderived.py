
import tmcmc

STARTFILE = 'STARTPARAMS.TEST.data'     # input
MCMCfile = 'MCMC.TEST.mcmc'             # input
DerivedFile = 'DERIVED.TEST.mcmc'       # output
tmcmc.myderivedfunc.printDerived_MTQ_2011(STARTFILE,MCMCfile,DerivedFile)

MCMCfile = 'cropMCMC.TEST.mcmc'             # input
DerivedFile = 'cropDERIVED.TEST.mcmc'       # output
tmcmc.myderivedfunc.printDerived_MTQ_2011(STARTFILE,MCMCfile,DerivedFile)

