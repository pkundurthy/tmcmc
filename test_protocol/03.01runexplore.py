
import tmcmc

def setALLFalse(ModelParams):
    """
    """
    
    for par in ModelParams.keys():
        ModelParams[par]['open'] = False
        
    return ModelParams

# Read data
ObservedData = tmcmc.mcmc.ReadMultiList('lclist.ls')
NuisanceData = tmcmc.mcmc.ReadDetrendFile('NUS.ONOFF.data')

# Read Start and Bound Parameter files
ModelParams = tmcmc.iomcmc.ReadStartParams('START.data')
BoundParams = tmcmc.iomcmc.ReadBoundFile('BOUNDS.TEST.data')

# Get the set of open parameters
TrueParams = []
for par in ModelParams.keys():
    if ModelParams[par]['open']:
        TrueParams.append(par)
        
NexploreSteps = 4e4
func = 'MTQ_multidepth_tduration'

for par in TrueParams:
    ModelParams = setALLFalse(ModelParams)
    ModelParams[par]['open'] = True
    tmcmc.mcmc.mcmc_mh_adapt(NexploreSteps,func,\
    ObservedData,ModelParams,NuisanceData,\
    BoundParams,False,False,\
    'EXPLORE.TEST.'+par+'.mcmc',\
    True)

os.system('ls EXPLORE*.mcmc > ExploreList.ls')