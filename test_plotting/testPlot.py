import tmcmc
from tmcmc.iomcmc import ReadStartParams

# The parameters you want on the x-axis (from left to right)
xp = ['D.T1.T2.T3','T0.T3','T0.T2','T0.T1','tG','tT']

# The parameters you want on the y-axis (top bottom to top)
yp = ['T0.T3','T0.T2','T0.T1','tG','tT']
yp = list(reversed(yp))
print yp

# For the above set a nested loop will assign the grid positions to the plots
MCMCGrid = {}
#This popylates the lower left end of the grid
for iy in range(len(yp)):
    for ix in range(len(xp)):
        if not ix >= iy:
            MCMCGrid[(ix,iy)] = (xp[ix],yp[iy])

# MCMC file
DataFile = 'test1.mcmc'

# Prep the transit data for the MCMC plots
AllPars = xp
AllPars.extend(yp)
AllPars = list(set(AllPars))

# Apply transit format, and modify data to preffered units
# the 3 dictionaries initiated below are useful for setting 
# your own axis Formats plotTransit.py has some functions to make
# some expected transformation to Transit parameters for MTQ_2011
par1 = ReadStartParams('FIT1.par')
par2 = ReadStartParams('FIT2.par')
parLabelFormat = tmcmc.plotTransit.TransitParFormat(AllPars)
parData, axisProperties = tmcmc.plotTransit.PrepTransitData(AllPars,DataFile,par1)

#also adjust the parameter values from the fits
par1new = par1.copy()
for par in par1.keys():
    par1new[par]['value'] = tmcmc.plotTransit.Tdata([par1[par]['value']],\
                            par,par1[par]['value'])
    par2[par]['value'] = tmcmc.plotTransit.Tdata([par2[par]['value']],\
                            par,par1[par]['value'])

# Initiate Figures
p = tmcmc.plotmcmc.triplot(MCMCGrid,DataFile)

# add Fits to plot
p.addFits('minuit',par2,markertype='o',markercolor='b',UseError=True)
p.addFits('mcmc',par1,markertype='o',markercolor='k',UseError=False)

# optional changes to parameter labels
p.generateAxisText(parformat=parLabelFormat)

# axis number properties set here, kw = axisform
p.generateAxisProperties(axisform=axisProperties)

#send parameters into plotter and make plot
p.initPlots(data=parData,hist='True')
p.makePlot()
#p.makePlot(OutFile='PlotName.eps')
