
import tmcmc

# Read data
ObservedData = tmcmc.mcmc.ReadMultiList('lclist.ls')
NuisanceData = tmcmc.mcmc.ReadDetrendFile('NUS.ONOFF.data')

# Read Start and Bound Parameter files
ModelParams = tmcmc.iomcmc.ReadStartParams('STARTPARAMS.TEST.data')
BoundParams = tmcmc.iomcmc.ReadBoundFile('BOUNDS.TEST.data')
    
##SHIFT starting point
#ShiftFactor = 15e0
##ShiftFactor = -15e0
#for Param in ModelParams.keys():
    #if ModelParams[Param]['open']:
        #ModelParams[Param]['value'] +=\
        #ShiftFactor*ModelParams[Param]['step']


Nsteps = 2e6
func = 'MTQ_multidepth_tduration'

tmcmc.mcmc.mcmc_mh_adapt(Nsteps,func,\
    ObservedData,ModelParams,NuisanceData,\
    BoundParams,False,True,\
    'MCMC.TEST.mcmc',\
    True)