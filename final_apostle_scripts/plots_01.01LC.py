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

def plot_Fit(ObjectName,Case,fitNum, **kwargs):
    
    Object = cfp.Object(ObjectName)
    Object.InitiateCase(Case)
    Object.InitiateFitNum(fitNum)
    Object.UpdateModelParams()
    Object.InitiateData()
    Object.HiResModelLC()
    print 'Object Initiated'
    
    fileNameRoot = cfp.PaperFiguresPath+'LCPlot.'+Object.name+'.'+Object.case+'.'+Object.fitNum
    for key in kwargs:
        if key.lower().startswith('filename'):
            fileNameRoot = kwargs[key]

    p = cfp.PlotPrep(Object)
    p.initLCPlotData()

    iCount = 1
    NTT = 0
    fig = plt.figure(figsize=(8,8))

    for TT in Object.ObservedData.keys():
        if TT.startswith('T'): NTT += 1

    if Object.name == 'TRES3':
        Nvert = 6
        ylim = (0.96,1.025)
        yticks = (0.97,0.985,1.0,1.015)
    else:
        Nvert = 5
        ylim = (0.975,1.02)
        yticks = (0.985,1.0,1.015)
        
    OrderTTList = []
    for i in range(NTT):
        OrderTTList.append('T'+format(i+1,'.0f'))

    TitleString = 'APOSTLE Observations of %s' % Object.name
    ypanel = 0
    for TT in OrderTTList:
        if TT.startswith('T'):
            plt.subplot(Nvert,2,iCount)

            xpanel = (iCount+1)%2
            #print '(',xpanel, ypanel,')', iCount
            plt.plot(p.PlotData[TT]['x'],p.PlotData[TT]['ydt'],'k.')
            plt.errorbar(p.PlotData[TT]['x'],p.PlotData[TT]['ydt'],yerr=p.PlotData[TT]['yerrdt'],fmt=None,ecolor='black')

            plt.plot(p.PlotData[TT]['xhiresmod'],p.PlotData[TT]['yhiresmod'],color='grey',linestyle='-',linewidth=2)
            ##plt.plot(p.PlotData[TT]['xmod'],p.PlotData[TT]['ymod'],'y-',linewidth=2)
            plt.ylim(ylim)
            plt.xlim((-0.175,0.175))
            Tsym = tmcmc.plotTransit.returnTsub(TT)
            plt.text(0.05,1.01,Tsym+' '+Object.Dates[TT])

            if ypanel == 0 and iCount == 1:
                plt.suptitle(TitleString,fontsize=14,y=0.93,ha='center')
            if xpanel == 0:
                plt.setp(plt.gca(),yticks = yticks )
            if xpanel == 1:
                plt.setp(plt.gca(),yticks =[])

            if Object.name == 'TRES3':
                if (xpanel == 1 and ypanel == 4) or (xpanel == 0 and ypanel == 5): 
                    plt.setp(plt.gca(),xticks= (-0.15,-0.075,0,0.075,0.15) )
                    plt.setp(plt.gca(),xlabel= r'BJD - Mid Transit Time (days)')
                else:
                    plt.setp(plt.gca(),xticks=[])
            else:
                if (xpanel == 1 and ypanel == 4) or (xpanel == 0 and ypanel == 4): 
                    plt.setp(plt.gca(),xticks= (-0.15,-0.075,0,0.075,0.15) )
                    plt.setp(plt.gca(),xlabel= r'BJD - Mid Transit Time (days)')
                else:
                    plt.setp(plt.gca(),xticks=[])

            if xpanel == 0 and ypanel == Nvert//2e0:
                plt.setp(plt.gca(),ylabel= r'Normalized Flux Ratio + offsets')

            if xpanel == 1:
                ypanel += 1

            iCount += 1

    plt.subplots_adjust(wspace=0)
    plt.subplots_adjust(hspace=0)
    #plt.show()
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
    parser.add_option('-c','--case',\
                      dest = 'Case',\
                      default = 'MCMC.FLD',\
                      help = 'fit case MINUIT.(FLD,OLD or MDFLD) or MCMC.(FLD,OLD or MDFLD)'\
                      )
    parser.add_option('-p','--plotfilename',\
                      dest = 'fname',\
                      default = None,\
                      help = ''\
                      )

    (opts,args) = parser.parse_args()
    if opts.fname != None:
        kwargs['filename'] = fname 

    print 'test plot ',ObjectName,opts.Case,opts.fitNum
    plot_Fit(ObjectName,opts.Case,opts.fitNum,**kwargs)
