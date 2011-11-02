import tmcmc
from tmcmc.iomcmc import ReadStartParams
import sys
import itertools

# The parameters you want on the x-axis (from left to right)
xp = ['D.T1.T2.T3','T0.T1','T0.T2']
yp = ['T0.T3','T0.T2','T0.T1']
# The parameters you want on the y-axis (top bottom to top)
# yp = list(reversed(yp))

# 
MCMCGrid = {(0,2):(xp[0],yp[2]),\
            (0,1):(xp[0],yp[1]),(1,1):(xp[1],yp[1]),\
            (0,0):(xp[0],yp[0]),(1,0):(xp[1],yp[0]),(2,0):(xp[2],yp[0])}

#print MCMCGrid
# MCMC file
DataFile = 'test1.mcmc'

# Prep the transit data for the MCMC plots
AllPars = []
for el in xp:
    AllPars.append(el)
for el in yp:
    AllPars.append(el)
    
AllPars = list(set(AllPars))

# Apply transit format, and modify data to preffered units
# the 3 dictionaries initiated below are useful for setting 
# your own axis Formats plotTransit.py has some functions to make
# some expected transformation to Transit parameters for MTQ_2011
par1 = ReadStartParams('FIT1.par')
par2 = ReadStartParams('FIT2.par')
parLabelFormat = tmcmc.plotTransit.TransitParFormat(AllPars)
parData, axisProperties = tmcmc.plotTransit.PrepTransitData(DataFile,AllPars,par1)

#using par1new
#print min(parData['T0.T2']), max(parData['T0.T2'])
#print axisProperties['T0.T2']['range']
#print axisProperties['T0.T2']['axisTicks']

#also adjust the parameter values from the fits
par1new = par1.copy()
for par in par1.keys():
    par1new[par]['value'] = tmcmc.plotTransit.TData([par1[par]['value']],\
                            par,par1[par]['value'])
    par2[par]['value'] = tmcmc.plotTransit.TData([par2[par]['value']],\
                            par,par1[par]['value'])

#print parLabelFormat.keys()
#print parLabelFormat

#sys.exit()

# Initiate Figures
#print len(xp), len(yp), 'what?'
p = tmcmc.plotmcmc.triplot(MCMCGrid,DataFile,xp,yp)

# add Fits to plot
p.addFits('minuit',par2,markertype='o',markercolor='b',UseError=True)
p.addFits('mcmc',par1,markertype='o',markercolor='k',UseError=False)

# optional changes to parameter labels
p.generateAxisText(parformat=parLabelFormat)

# axis number properties set here, kw = axisform
p.generateAxisProperties(axisform=axisProperties)

#send parameters into plotter and make plot
p.initPlots(data=parData,hist=True)
p.makePlot()
#p.makePlot(plotfile='PlotName.eps')
