#!/astro/apps/pkg/python64/bin//python

import tmcmc
from tmcmc import class_fitprep as cfp
import sys
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
fig = plt.figure(figsize=(8,8))

def plot_Fit(ObjectName,Case,fitNum):
    
    Object = cfp.Object(ObjectName)
    Object.InitiateCase(Case)
    Object.InitiateFitNum(fitNum)
    Object.UpdateModelParams()
    Object.InitiateData()
    Object.HiResModelLC()
    
    p = cfp.PlotPrep(Object)
    p.initLCPlotData()

    iCount = 1
    NTT = 0
    fig = plt.figure(figsize=(8,8))

    for TT in Object.ObservedData.keys():
        if TT.startswith('T'): NTT += 1
        
    if Object.name == 'TRES3':
        Nvert = 6
    else:
        Nvert = 5

    ypanel = 0
    for TT in Object.ObservedData.keys():
        if TT.startswith('T'):
            plt.subplot(Nvert,2,iCount)
            xpanel = (iCount+1)%2
            #print '(',xpanel, ypanel,')', iCount
            plt.plot(p.PlotData[TT]['x'],p.PlotData[TT]['ydt'],'b.')
            plt.errorbar(p.PlotData[TT]['x'],p.PlotData[TT]['ydt'],yerr=p.PlotData[TT]['yerrdt'],fmt=None)
            
            plt.plot(p.PlotData[TT]['x'],p.PlotData[TT]['yobs']-0.02,'r.')
            plt.errorbar(p.PlotData[TT]['x'],p.PlotData[TT]['yobs']-0.02,yerr=p.PlotData[TT]['yerrobs'],fmt=None)
            
            plt.plot(p.PlotData[TT]['xhiresmod'],p.PlotData[TT]['yhiresmod'],'g-',linewidth=2)
            plt.ylim((0.95,1.025))
            plt.xlim((-0.175,0.175))
            plt.text(0,1.01,p.Dates[TT])
            
            if ypanel == 0 and iCount == 1:
                plt.suptitle('APOSTLE Observations of %s' % Object.name)
            if xpanel == 0:
                plt.setp(plt.gca(),yticks = (0.96,0.98,1.0,1.02) )
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
    plt.savefig(cfp.FigurePath+'TestAll.'+Object.name+'.'+Object.case+'.'+Object.fitNum+'.png')
    
if __name__ == '__main__':
    
    #ObjectName = sys.argv[1] 
    #Case = sys.argv[2]
    #fitNum = sys.argv[3]
    
    for ObjectName in ['TRES3','WASP2','XO2']:
        for Case in ['MINUIT.FLD']:
            for fitNum in [1,2]:
                print 'test plot ',ObjectName,Case,fitNum
                plot_Fit(ObjectName,Case,fitNum)
    