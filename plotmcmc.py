
import matplotlib
import sys
import numpy as np
import scipy
import scipy.ndimage
from matplotlib import pyplot as plt
from iopostmcmc import isNonParam, read1parMCMC, getPars
from iomcmc import ReadStartParams
from binning import MedianMeanOutlierRejection
from matplotlib import pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from matplotlib.font_manager import fontManager, FontProperties

def returnTsub(TSTAMP):
    """ For a parameter with transit time tag, 
    return latex symbol 
    """
    
    if TSTAMP.startswith('T'):
        Tnum = TSTAMP.strip('T').strip('0.').strip('T')
        Tsub = '$T_{%s}$' % Tnum
    else:
        Tsub = 'Wrong'
        
    return Tsub

def rangeMidpoints(x):
    """
    compute and return list of mid-points
    of a given discrete function
    """
    
    newx = []
    for i in range(len(x)-1):
        newx.append(0.5e0*(x[i]+x[i+1]))

    return np.array(newx)

def return1Dfrom2D(arr2D):
    """
    return 1D array from a 2D array
    """
    
    arr1D =  arr2D.reshape(-1) 
    return arr1D

def singleJC(data1,data2):
    """ make a single Joint-Correlation plot 
    from single parameter dictionaries """
    
    new_data = {}
    for key in data1.keys():
        if not isNonParam(key):
            par1 = key
            new_data[par1] = data1[par1]
    for key in data2.keys():
        if not isNonParam(key):
            par2 = key
            new_data[par2] = data2[par2]
            
    JC(par1,par2,new_data)

def JC(par1,par2,dataMCMC):
    """ make a single Joint-Correlation plot """
    
    x = np.array(dataMCMC[par1])
    y = np.array(dataMCMC[par2])

    sigma_arr = np.array([1e0,2e0,3e0,4e0,5e0])
    levels = scipy.special.erf(sigma_arr/np.sqrt(2e0))
    
    hist2D,xedge,yedge = np.histogram2d(x,y,bins=25)
    hist2D = np.transpose(hist2D)
    
    histlist = return1Dfrom2D(hist2D)
    hist_sort = np.sort(histlist)
    hist_sort_rev = hist_sort[::-1]
    cummul_sum = np.cumsum(hist_sort_rev)
    
    xlev = []
    maxcsum = np.max(cummul_sum)
    for j in range(len(levels)):
        for i in range(len(cummul_sum)):
            el = np.abs(cummul_sum[i]-levels[j]*maxcsum)
            if i == 0:
                minel = el
                imin = i
            if i > 0:
                if minel > el:
                    minel = el
                    imin = i
        xlev.append(imin)

    levelID = []
    for xl in xlev[::-1]:
        levelID.append(hist_sort_rev[long(xl)])
    
    clev = levelID 
    #print clev
    x1 = np.array(xedge.tolist())
    y1 = np.array(yedge.tolist())
    xarr = rangeMidpoints(x1)
    yarr = rangeMidpoints(y1)
    
    cmap = matplotlib.colors.Colormap('jet',N=5)
    sig_labels = (r'1-$\sigma$',r'2-$\sigma$',r'3-$\sigma$',r'4-$\sigma$',r'5-$\sigma$')
    sig_labels = sig_labels[::-1]
    clevel = {}
    newlev = []
    #print sig_labels
    #print clev
    for i in range(len(sig_labels)):
        clevel[clev[i]] = sig_labels[i]
        newlev.append(clev[i])
    clevel[0] = ''
    #newlevalt = newlev.copy()
    newlev.append(0)
    colortup = ('#FF6600','#FF9900','#FFCC00','#FFFF00','#FFFF99')
    smooth2D = scipy.ndimage.filters.median_filter(hist2D,size=3)
    #extent = [yedge[0],yedge[-1],xedge[-1],xedge[0]]
    CSV = plt.contourf(xarr,yarr,smooth2D,levels=newlev,colors=colortup)
    CS = plt.contour(xarr,yarr,smooth2D,levels=newlev[:-1],colors='k')
    plt.clabel(CS,inline=1,fontsize=12,fmt=clevel)
    #cb = plt.colorbar(CSV)
    return plt.figure
    
    
def checkFormatTT(data,parName,**kwargs):
    """
        Format data and labels for transit timing MCMC
    """
    
    #check for param files
    for key in kwargs:
        if key.lower().startswith('lowchi'):
            par1 = ReadStartParams(kwargs[key])
        elif key.lower().startswith('minuit'):
            par2 = ReadStartParams(kwargs[key])
        else:
            print 'No params files recognized'
            sys.exit()
    
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

def robust1sigma(x):
    """
    return 1-sigma
    """
    x = x-np.median(x)
    dsort = np.sort(x)
    npts = len(x)
    sigma = (x[.8415*npts]-x[.1585*npts])/2e0
    
    return sigma

def getPlotLoc(d1,d2,spaceTopR):
    """
    
    """
    
    d1 = np.array(d1)
    d2 = np.array(d2)
    mm1, sdv1, ngood1, goodindex1, badindex1 = MedianMeanOutlierRejection(d1, 5, 'median')
    mm2, sdv2, ngood2, goodindex2, badindex2 = MedianMeanOutlierRejection(d2, 5, 'median')
    #print np.shape(goodindex1), np.shape(goodindex2), np.shape(d1), np.shape(d2)
    
    xrg = (min(d1[goodindex1]), max(d1[goodindex1]))
    yrg = (min(d2[goodindex2]), max(d2[goodindex2]))
    #xrg = (np.median(d1)-10*sigma1,np.median(d1)+10*sigma1)
    #yrg = (np.median(d2)-10*sigma2,np.median(d2)+10*sigma2)
    
    xrg0 = xrg[0]
    yrg0 = yrg[0]
    xrg1 = spaceTopR*(xrg[1]-xrg[0])+xrg[0]
    yrg1 = spaceTopR*(yrg[1]-yrg[0])+yrg[0]
                
    xpos = np.zeros(3)+(0.70*(xrg1-xrg0) + xrg0)
    ypos = np.linspace(0.70,0.90,3)*(yrg1-yrg0) + yrg0
    
    return xrg0,xrg1,yrg0,yrg1,xpos,ypos

def trianglePlotTT(DataFile,Stats,spaceTopR,**kwargs):
    """
    
    """
    
    parList = getPars(DataFile)
    Npar = len(parList)
    iplot = 1
    nyticks = 2
    nxticks = 2
    
    for key in kwargs:
        if key.lower().startswith('lowchi'):
            fit1 = kwargs[key]
        elif key.lower().startswith('minuit'):
            fit2 = kwargs[key]
        else:
            print 'No params files recognized'
            sys.exit()

    for iy in range(Npar):
        for ix in range(Npar):
            if not ix >= iy:
                parName1 = parList[ix]
                parName2 = parList[iy]
                plt.subplot(Npar-1,Npar-1,iplot)
                d1 = read1parMCMC(DataFile,parName1)
                d2 = read1parMCMC(DataFile,parName2)
                
                d1,parSym1,axF1,Odata1 = \
                checkFormatTT(d1,parName1,\
                lowchi=fit1,minuit=fit2)
                
                d2,parSym2,axF2,Odata2 = \
                checkFormatTT(d2,parName2,\
                lowchi=fit1,minuit=fit2)
                
                xrg0, xrg1, yrg0, yrg1, xpos, ypos = \
                getPlotLoc(d1[parName1],d2[parName2],spaceTopR)
                
                fig = singleJC(d1,d2)
                
                cov = r'$|\sigma_{(x,y)}|$='+\
                format(abs(Stats['cov'][parName1][parName2]['value']),'0.2f')
                
                spe = r'$|\rho|$='+\
                format(abs(Stats['spear'][parName1][parName2]['value']),'0.2f')
                
                pea = r'$|r|$='+\
                format(abs(Stats['pear'][parName1][parName2]['value']),'0.2f')
                
                yticks = tuple([0.75*yrg0+0.25*yrg1,0.25*yrg0+0.75*yrg1])
                xticks = tuple([0.75*xrg0+0.25*xrg1,0.25*xrg0+0.75*xrg1])
                plt.setp(plt.gca(), yticks=yticks,xticks=xticks)
                #supress xtick labels for plots not at bottom
    
                plt.xlim([xrg0,xrg1])
                plt.ylim([yrg0,yrg1])
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
                
                plt.plot(Odata1['lowchi']['data'],Odata2['lowchi']['data'],'ko',label='MCMC')
                plt.plot(Odata1['minuit']['data'],Odata2['minuit']['data'],'bo',label='Minuit')
                plt.errorbar(Odata1['minuit']['data'],Odata2['minuit']['data'],\
                yerr=Odata2['minuit']['err'],xerr=Odata1['minuit']['err'],fmt=None)
                
                plt.text(xpos[0],ypos[0],cov)
                plt.text(xpos[1],ypos[1],spe)
                plt.text(xpos[2],ypos[2],pea)
                plt.subplots_adjust(hspace=0)
                plt.subplots_adjust(wspace=0)
                
            if iy != 0 and ix != Npar-1:
                iplot += 1
                
    #plt.subplot(Npar-1,Npar-1,Npar-1)
    #plt.axis('off')
    LegFont = FontProperties(size=16)
    plt.legend( ('MCMC','Minuit'), numpoints=1,loc='center',\
    prop=LegFont, bbox_to_anchor=(0.6,1.5) )

    plt.show()
