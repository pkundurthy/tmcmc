
import tmcmc
import sys
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import FormatStrFormatter

fileMCMC = 'test1.mcmc'
#fileMCMC = 'MCMC4plot.mcmc'

parList = tmcmc.iopostmcmc.getPars(fileMCMC)
#print parList
parList = parList[0:3]
Npar = len(parList)
iplot = 1
nyticks = 2
nxticks = 2

par1 = tmcmc.iomcmc.ReadStartParams('FIT1.par')
par2 = tmcmc.iomcmc.ReadStartParams('FIT2.par')

def returnTsub(TSTAMP):
    
    if TSTAMP.startswith('T'):
        Tnum = TSTAMP.strip('T').strip('0.').strip('T')
        Tsub = '$T_{%s}$' % Tnum
    else:
        Tsub = 'Wrong'
        
    return Tsub

def checkFormat(data,parName):
    
    if parName.startswith('T0'):
        x = ((np.array(data[parName]) - par1[parName]['value'])*86400e0).tolist()
        data[parName] = x
        p2d = (par2[parName]['value'] - par1[parName]['value'])*86400e0
        Odata = {'lowchi':{'data':[-9e9,0]},\
                  'minuit':{'data':[-9e9,p2d],\
                  'err':[0,par2[parName]['step']*86400e0]} }
        parSym = '$T_{mid}$ - '+returnTsub(parName)
        AxFormat = FormatStrFormatter('%.3f')
    elif parName.startswith('D'):
        msplit = map(str,parName.split('.'))
        TT = ''
        for j in range(len(msplit)):
            if j > 0:
                TT += returnTsub(msplit[j]).strip('$')+' '
        Odata = {'lowchi':{'data':[-9e9,par1[parName]['value']]},\
            'minuit':{'data':[-9e9,par2[parName]['value']],\
            'err':[0,par2[parName]['step']]} }
        parSym = '$'+msplit[0]+'_{(%s)}$' % TT
        AxFormat = FormatStrFormatter('%.4f')
    elif parName == 'tG':
        Odata = {'lowchi':{'data':[-9e9,par1[parName]['value']]},\
        'minuit':{'data':[-9e9,par2[parName]['value']],\
        'err':[0,par2[parName]['step']]} }
        parSym = r'$\tau_{G}$'
        AxFormat = FormatStrFormatter('%.4f')
    elif parName == 'tT':
        Odata = {'lowchi':{'data':[-9e9,par1[parName]['value']]},\
        'minuit':{'data':[-9e9,par2[parName]['value']],\
        'err':[0,par2[parName]['step']]} }
        parSym = r'$\tau_{T}$'
        AxFormat = FormatStrFormatter('%.4f')
    else:
        Odata = {'lowchi':{'data':[-9e9,par1[parName]['value']]},\
        'minuit':{'data':[-9e9,par2[parName]['value']],\
        'err':[0,par2[parName]['step']]} }
        parSym = parName
        AxFormat = None

    return data, parSym, AxFormat, Odata

#print parList
for iy in range(Npar):
    for ix in range(Npar):
        if not ix >= iy:
            parName1 = parList[ix]
            parName2 = parList[iy]
            plt.subplot(Npar-1,Npar-1,iplot)
            d1 = \
            tmcmc.postmcmc.read1parMCMC(fileMCMC,parName1)
            d2 = \
            tmcmc.postmcmc.read1parMCMC(fileMCMC,parName2)
            d1,parSym1,axF1,Odata1= checkFormat(d1,parName1)
            d2,parSym2,axF2,Odata2 = checkFormat(d2,parName2)
            xrg = min(d1[parName1]), max(d1[parName1])
            yrg = min(d2[parName2]), max(d2[parName2])
            fig = tmcmc.plotmcmc.singleJC(d1,d2)
            cy = np.median( [yrg[0],yrg[1]] )
            cx = np.median( [xrg[0],xrg[1]] )
            plt.plot(Odata1['lowchi']['data'],Odata2['lowchi']['data'],'ko')
            plt.plot(Odata1['minuit']['data'],Odata2['minuit']['data'],'bo')
            plt.errorbar(Odata1['minuit']['data'],Odata2['minuit']['data'],\
            yerr=Odata2['minuit']['err'],xerr=Odata1['minuit']['err'],fmt=None)
            #plt.text(cx,cy,str(iplot))
            #yticks = tuple(np.linspace(yrg[0],yrg[1],nyticks))
            #xticks = tuple(np.linspace(xrg[0],xrg[1],nxticks))
            yticks = tuple([0.75*yrg[0]+0.25*yrg[1],0.25*yrg[0]+0.75*yrg[1]])
            xticks = tuple([0.75*xrg[0]+0.25*xrg[1],0.25*xrg[0]+0.75*xrg[1]])
            plt.setp(plt.gca(), yticks=yticks,xticks=xticks)
            #supress xtick labels for plots not at bottom
            plt.xlim([xrg[0],xrg[1]])
            plt.ylim([yrg[0],yrg[1]])
            #print iplot, xrg, yrg
            if iy != Npar-1:
                plt.setp(plt.gca(), xticklabels=[])
                #print ' no x ', iplot
                #pass
            #supress ytick labels for plots not at left corner
            if ix != 0:
                plt.setp(plt.gca(), yticklabels=[])
                #print ' no y ', iplot
                #pass
            #print xlabels for bottom row
            if iy == Npar-1:
                plt.xlabel(parSym1, fontsize=16)
                if axF1 != None:
                    plt.setp(plt.gca().xaxis.set_major_formatter(axF1))
            #print ylabels for left corner column
            if ix == 0:
                plt.ylabel(parSym2, fontsize=16)
                if axF2 != None:
                    plt.setp(plt.gca().yaxis.set_major_formatter(axF2))
            plt.subplots_adjust(hspace=0)
            plt.subplots_adjust(wspace=0)
        if iy != 0 and ix != Npar-1:
            iplot += 1
            #print i

plt.show()
        