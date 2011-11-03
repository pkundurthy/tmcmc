import tmcmc
from tmcmc.iomcmc import ReadStartParams
import sys
import itertools

# The parameters you want on the x-axis (from left to right)
xp = ['D.T1.T2.T3','T0.T1','T0.T2']
# The parameters you want on the y-axis (bottom to top)
yp = ['T0.T3','T0.T2','T0.T1']

# The Grid assignment plot
#MCMCGrid2 = {(0,2):(xp[0],yp[2]),\
            #(0,1):(xp[0],yp[1]),(1,1):(xp[1],yp[1]),\
            #(0,0):(xp[0],yp[0]),(1,0):(xp[1],yp[0]),(2,0):(xp[2],yp[0])}

MCMCGrid = tmcmc.plotmcmc.SimplifyGrid(xp,yp)
#print MCMCGrid2
#print '---'
#print MCMCGrid

# MCMC file
DataFile = 'test1.mcmc'
#DataFile = 'MCMC4plot.mcmc'

# Prep the transit data for the MCMC plots
AllPars = list(set(xp+yp))

# Apply transit format, and modify data to preffered units
# the 3 dictionaries initiated below are useful for setting 
# your own axis Formats plotTransit.py has some functions to make
# some expected transformation to Transit parameters for MTQ_2011
par1 = ReadStartParams('FIT1.par')
par2 = ReadStartParams('FIT2.par')
parLabelFormat = tmcmc.plotTransit.TransitParFormat(AllPars)
parData, axisProperties = tmcmc.plotTransit.PrepTransitData(DataFile,AllPars,par1)

#also adjust the parameter values from the fits
par1new = par1
for par in par1.keys():
    if par.startswith('T0'):
        par2[par]['value'] = (par2[par]['value'] -par1[par]['value'])*86400e0
        par2[par]['step'] = (par2[par]['step'])*86400e0
        par1new[par]['value'] = (par1new[par]['value'] -par1[par]['value'])*86400e0
        par1new[par]['step'] = (par1new[par]['step'])*86400e0

# Initiate Figures
p = tmcmc.plotmcmc.triplot(MCMCGrid,DataFile,xp,yp)

# add Fits to plot
#for par in par2.keys():
    #print par, par2[par]['value'], par1new[par]['step']

#sys.exit()
p.addFits('minuit',par2,markertype='o',markercolor='b',UseError=True)
p.addFits('mcmc',par1new,markertype='o',markercolor='k',UseError=False)

# optional changes to parameter labels
p.generateAxisText(parformat=parLabelFormat)

# axis number properties set here, kw = axisform
p.generateAxisProperties(axisform=axisProperties)

# send parameters into plotter and make plot
p.initPlots(data=parData,hist=True,binhist=50)

# p.makePlot()
p.makePlot(fsizex=16,fsizey=16,legfontsz=16)
