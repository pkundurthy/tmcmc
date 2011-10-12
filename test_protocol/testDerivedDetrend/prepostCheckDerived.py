
# derived

import tmcmc

STARTFILE = 'STARTPARAMS.TEST.data'             # input
MCMCfile = 'MCMC_der.TEST.mcmc'                 # input
DerivedFilePost = 'DERIVED_derPost.TEST.mcmc'   # output
tmcmc.myderivedfunc.printDerived_MTQ_2011(STARTFILE,MCMCfile,DerivedFile)

DerivedFilePre = 'DERIVED_der.TEST.mcmc'


