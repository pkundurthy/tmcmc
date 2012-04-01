#!/astro/apps/pkg/python64/bin//python

import os
import tmcmc
from tmcmc import class_fitprep as cfp
import sys
import optparse
import pylab as plt
import numpy as num
from matplotlib import rc
import matplotlib
from matplotlib import legend
rc('font',**{'family':'serif','serif':['Times New Roman'],'style':'semibold'})
rc('text',usetex=True)
from matplotlib.ticker import FormatStrFormatter,MaxNLocator, FixedLocator

width, height = matplotlib.rcParams['figure.figsize']
#print width, height
ObjectList = cfp.ObjectList

def plotMCMC(ObjectName,Case,fitNum,parList, **kwargs):

    Object = cfp.Object(ObjectName)
    Object.InitiateCase(Case)
    Object.InitiateFitNum(fitNum)
    Object.UpdateModelParams()
    print 'Object Initiated'

    xp = parList[:-1]
    yp = parList[::-1][:-1]

    fileNameRoot = cfp.PaperFiguresPath+'MCMCTriplot.'+\
                   Object.name+'.'+Object.case+'.'+Object.fitNum

    FitList = []
    for key in kwargs:
        if key.lower().startswith('filename'):
            fileNameRoot = kwargs[key]
        if key.lower().startswith('yparlist'):
            xp = parList
            yp = kwargs[key]
        if key.lower().startswith('tag'):
            fileNameRoot = cfp.PaperFiguresPath+'MCMCTriplot.'+Object.name+\
                           '.'+Object.case+'.'+Object.fitNum+'.'+tag
        if key.lower().startswith('otherfits'):
            FitList = kwargs[key]

    p = cfp.PlotPrep(Object)
    p.initMCMCPlot(xp,ypars=yp,useshort=True)

    AllPars = list(set(p.xpars+p.ypars))
    # required to plot points on triplot
    parErrMain = tmcmc.iopostmcmc.readErrorFile(p.ErrorFiles[0])
    parErrDerived = tmcmc.iopostmcmc.readErrorFile(p.ErrorFiles[1])

    # identical Key check
    for key in  parErrMain.keys():
        if key in parErrDerived.keys():
            raise NameError("Identical keys in MCMC and derived data - should not happen")

    ParErr = dict(parErrMain.items()+parErrDerived.items())
    parData, axisProperties = tmcmc.plotTransit.PrepTransitData(p.MCMCFiles,AllPars,ParErr)

    ParErr = tmcmc.plotTransit.parErr4Plot(ParErr)
    parErrPlot = tmcmc.plotTransit.parTimeDay2Sec(ParErr,Object.ModelParams)
    parLabelFormat = tmcmc.plotTransit.TransitParFormat(AllPars,objectname=p.Object.name)

    fitLabel,mtype,mcolor = tmcmc.plotTransit.FitLabels(p.Object.case)
    p.triplot.addFits(fitLabel,parErrPlot,markertype=mtype,markercolor=mcolor,UseError=True)

    # add other fits
    p.OtherFits(FitList)
    for Case in p.OtherParErr.keys():
        p.triplot.addFits(p.OtherParErr[Case]['fitLabel'],\
                          p.OtherParErr[Case]['pdict'],\
                          markertype=p.OtherParErr[Case]['mtype'],\
                          markercolor=p.OtherParErr[Case]['mcolor'],\
                          UseError=True)

    # optional changes to parameter labels
    p.triplot.generateAxisText(parformat=parLabelFormat)

    # axis properties set here
    p.triplot.generateAxisProperties(axisform=axisProperties)

    # send parameters into plotter and make plot
    p.triplot.initPlots(data=parData,hist=True,binhist=25)

    #p.makePlot(legloc=(2.5,4))
    p.triplot.makePlot(plotfile=fileNameRoot+'.png',fsizex=14,fsizey=14,legfontsz=14)
    #p.triplot.makePlot(plotfile=fileNameRoot+'.eps',fsizex=14,fsizey=14,legfontsz=14)

if __name__ == '__main__':

    ObjectName = sys.argv[1]
    if len(sys.argv) == 1:
        ObjectName = ' '
    else:
        ObjectName = sys.argv[1]

    if ObjectName not in ObjectList:
        print 'could not recognize object...'
        raise NameError('Unrecognized object')

    kwargs = {}
    parser = optparse.OptionParser(usage=\
             "%prog ObjectName [mandatory] [optional folder condition]")

    parser.add_option('-f','--fitnum',\
                      dest = 'fitNum',\
                      default = 1,\
                      help = 'fit number 1 or 2'\
                      )
    parser.add_option('-l','--parlist',\
                      dest = 'parlist',\
                      default = "[]",\
                      help = 'list of parameters (default triplot)'\
                      )
    parser.add_option('-c','--case',\
                      dest = 'Case',\
                      default = 'MCMC.FLD',\
                      help = 'fit case MINUIT.(FLD,OLD or MDFLD) or MCMC.(FLD,OLD or MDFLD)'\
                      )
    parser.add_option('-y','--yparlist',\
                      dest = 'yparlist',\
                      default = None,\
                      help = 'list of parameters (default triplot)'\
                     )
    parser.add_option('-p','--plotfilename',\
                      dest = 'fname',\
                      default = None,\
                      help = 'name of plot file'\
                      )
    parser.add_option('-o','--otherfits',\
                      dest = 'otherfits',\
                      default = None,\
                      help = 'list of other fits to overplot'\
                      )
    parser.add_option('-t','--plottag',\
                      dest = 'tag',\
                      default = None,\
                      help = 'unique tag to identify plot'\
                      )

    (opts,args) = parser.parse_args()

    ParList = map(str, opts.parlist.strip('\"').strip("\'").split(','))
    if opts.yparlist == None:
        yParList = None
    else:
        yParList = map(str, opts.yparlist.strip('\"').strip("\'").split(','))
        kwargs['yparlist'] = yParList

    if opts.fname != None:
        kwargs['filename'] = opts.fname

    if opts.tag != None:
        kwargs['tag'] = opts.tag

    if opts.otherfits != None:
        FitList = map(str, opts.otherfits.strip('\"').strip("\'").split(','))
        kwargs['otherfits'] = FitList

    print 'MCMC ',ObjectName,opts.Case,opts.fitNum, ParList, kwargs
    plotMCMC(ObjectName,opts.Case,opts.fitNum,ParList,**kwargs)
