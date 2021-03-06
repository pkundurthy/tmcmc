import tmcmc
from tmcmc.iomcmc import ReadStartParams
import sys
import itertools

# The parameters you want on the x-axis (from left to right)
xp = ['D.T1.T2.T3','T0.T1','T0.T2']
# The parameters you want on the y-axis (bottom to top)
yp = ['T0.T3','T0.T2','T0.T1']

# The Grid assignment plot
MCMCGrid2 = {(0,2):(xp[0],yp[2]),\
             (0,1):(xp[0],yp[1]),(1,1):(xp[1],yp[1]),\
             (0,0):(xp[0],yp[0]),(1,0):(xp[1],yp[0]),(2,0):(xp[2],yp[0])}

#For a reasonable list you can also use SimplyGrid to generate the MCMCGrid
MCMCGrid = tmcmc.plotmcmc.SimplifyGrid(xp,yp)

# MCMC file
#DataFile = 'test1.mcmc'
DataFile = 'MCMC4plot.mcmc'

# Prepare the transit data for the MCMC plots
# modify T0 data to preferred units
# expected transformation for MTQ_2011 parameters
AllPars = list(set(xp+yp))
par1 = ReadStartParams('FIT1.par')
par2 = ReadStartParams('FIT2.par')
parErr = tmcmc.iopostmcmc.readErrorFile('Errors.par')

# the 3 dictionaries initiated below are useful for setting 
# axis Formats, labels etc...
parLabelFormat = tmcmc.plotTransit.TransitParFormat(AllPars)
parData, axisProperties = tmcmc.plotTransit.PrepTransitData(DataFile,AllPars,par1)

#also adjust the parameter values from the fits
par2 = tmcmc.plotTransit.parTimeDay2Sec(par2,par1)
parErr = tmcmc.plotTransit.parErr4Plot(parErr)
parErrPlot = tmcmc.plotTransit.parTimeDay2Sec(parErr,par1)
par1new = par1.copy()
par1new = tmcmc.plotTransit.parTimeDay2Sec(par1new,par1)

#for par in parErrPlot.keys():
    #print 'mcmc', par1new[par]['value'], 'errM', parErrPlot[par]['value'], 'Minuit', par2[par]['value']
    #print 'errM', parErrPlot[par]['step'], 'Minuit', par2[par]['step']

#sys.exit()
# Initiate Figures
p = tmcmc.plotmcmc.triplot(MCMCGrid,DataFile,xp,yp)

# add Fits to plot
p.addFits('Minuit',par2,markertype='o',markercolor='b',UseError=True)
p.addFits('MCMC',parErrPlot,markertype='o',markercolor='k',UseError=False)
#p.addFits('MCMC',par1new,markertype='o',markercolor='k',UseError=False)

# optional changes to parameter labels
p.generateAxisText(parformat=parLabelFormat)

# axis properties set here
p.generateAxisProperties(axisform=axisProperties)

# send parameters into plotter and make plot
p.initPlots(data=parData,hist=True,binhist=25)

#p.makePlot()
plotfile='MCMCtest.eps'
p.makePlot(plotfile=plotfile,fsizex=14,fsizey=14,legfontsz=14,legloc=(3,4))
