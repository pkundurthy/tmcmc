import tmcmc

ObservedData = tmcmc.mcmc.ReadMultiList('lclist.ls')
NuisanceData = tmcmc.mcmc.ReadDetrendFile('NUS.ONOFF.data')

# Read Start and Bound Parameter files
ModelParams = tmcmc.iomcmc.ReadStartParams('STARTPARAMS.TEST.data')
BoundParams = tmcmc.iomcmc.ReadBoundFile('BOUNDS.TEST.data')

OutFile = 'MINUITPARAMS.TEST.data'
tolnum = 3e4
FunctionName = 'MTQ_multidepth_tduration'

tmcmc.runminuit.RunMinuit(FunctionName,ObservedData,ModelParams,NuisanceData,BoundParams,tolnum,OutFile)
