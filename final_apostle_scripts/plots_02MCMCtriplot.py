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

    fileNameRoot = cfp.PaperFiguresPath+'MCMCTriplot.'+Object.name+'.'+Object.case+'.'+Object.fitNum
    for key in kwargs:
        if key.lower().startswith('filename'):
            fileNameRoot = kwargs[key]
        if key.lower().startswith('yparlist'):
            xp = parList
            yp = kwargs[key]

    p = cfp.PlotPrep(Object)
    p.initMCMCPlot(xp,ypars=yp)

    p.triplot.makePlot(plotfile=plotfile,fsizex=14,fsizey=14,legfontsz=14,legloc=(2.5,4))
    p.triplot.makePlot(plotfile=plotfile2,fsizex=14,fsizey=14,legfontsz=14,legloc=(2.5,4))

    plt.savefig(fileNameRoot+'.png')
    plt.savefig(fileNameRoot+'.eps')

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
                      default = "",\
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

    exec("ParList = [%s]" % opts.parlist.strip('\"').strip("\'"))
    exec("yParList = [%s]" % opts.yparlist.strip('\"').strip("\'"))

    (opts,args) = parser.parse_args()
    if opts.fname != None:
        kwargs['filename'] = fname
    if len(yparList) > 0:
        kwargs['yparlist'] = yParList

    print 'MCMC ',ObjectName,opts.Case,opts.fitNum
    plotMCMC(ObjectName,opts.Case,opts.fitNum,parList,**kwargs)
