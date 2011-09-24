
import tmcmc

ObservedData = tmcmc.mcmc.ReadMultiList('obs.list')
NuisanceData = {'GlobalSwitch':False}
ModelParams =  tmcmc.mcmc.ReadStartParams('STARTPARAMS.data')
BoundParams =  tmcmc.mcmc.ReadBoundsFile('BOUNDS.data')

tmcmc.mcmc.mcmc_mh_adapt(40000,'quad',ObservedData,ModelParams,NuisanceData,BoundParams,False,True,'MCMC_quad.test.data',True)

tmcmc.mcmc.WriteLowestChisq('MCMC_quad.test.data',ModelParams,'LOWESTCHISQPARAMS.data',True)

#Check ModelData and make a plot of priliminary guess (green) and the lowest-chisq parameter set from the MCMC (red) 
ModelParamsLoChi =  tmcmc.mcmc.ReadStartParams('LOWESTCHISQPARAMS.data')
ModelData = tmcmc.myfunc.quad(ModelParams,ObservedData)
ModelDataLoChi = tmcmc.myfunc.quad(ModelParamsLoChi,ObservedData)

from matplotlib import pyplot as plt
x = ObservedData['all']['x']
y = ObservedData['all']['y']
yerr = ObservedData['all']['yerr']
ymod0 = ModelData['all']['y']
ymod1 = ModelDataLoChi['all']['y']
plt.plot(x,y,'b.')
plt.plot(x,ymod0,'g-')
plt.plot(x,ymod1,'r-')
plt.show()
