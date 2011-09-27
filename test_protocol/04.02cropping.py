
import tmcmc
import os
import sys

CropFile = 'cropMCMC.TEST.mcmc'
MCMCfile = 'MCMC.TEST.mcmc'

# cropping
tmcmc.iopostmcmc.cropMCMC(MCMCfile,CropFile,0.05)
