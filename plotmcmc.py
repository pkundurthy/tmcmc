import sys
import numpy as np
import scipy
import scipy.ndimage
from iopostmcmc import isNonParam, read1parMCMC, getPars
from iomcmc import ReadStartParams, checkFileExists
from binning import MedianMeanOutlierRejection
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from matplotlib.font_manager import fontManager, FontProperties

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
    
def getRange(d,**kwargs):
    
    # default
    ext0 = 1
    ext1 = 1
    for key in kwargs:
        if key.lower() == 'ext0':
            ext0 = float(kwargs[key])
        elif key.lower() == 'ext1':
            ext1 = float(kwargs[key])
        else:
            continue

    d = np.array(d)
    mm, sdv, ngood, goodindex, badindex = \
    MedianMeanOutlierRejection(d,5,'median')
    
    rg = (min(d[goodindex]), max(d[goodindex]))
    
    rg0 = rg[0] - ext0*(rg[1]-rg[0])
    rg1 = rg[1] + ext1*(rg[1]-rg[0])
    
    return rg0,rg1
    
def axisTicks(rg0,rg1):
    """
    sets 2 ticks per MCMC plot axis
    """

    return tuple([0.75*rg0+0.25*rg1,0.25*rg0+0.75*rg1])

class triplot:

    def __init__(self,GridDict,MCMCFile):
        
        maxX = 0
        maxY = 0
        for key in GridDict:
            if key[0] > maxX:
                maxX = key[0]
            if key[1] > maxY:
                maxY = key[1]
            
        self.GridNX = maxX+1
        self.GridNY = maxY+1
        parList = []
        for ix in range(GridNX):
            for iy in range(GridNY):
                parList.append(GridDict[(ix,iy)][0])
                parList.append(GridDict[(ix,iy)][0])
                try:
                    dummy = GridDict[(ix,iy)]
                except:
                    GridDict[(ix,iy)] = None

        self.parList = list(set(parList))
        self.GridDict = GridDict
        self.MCMCFile = MCMCFile
        self.ParDict = {}
 
    def addFits(self,Label,parDict,**kwargs):
        
        mkt = 'o'
        mkc = 'r'
        UseErr = False
        try:
            dummy = self.Points
        except:
            self.Points = {}
        
        for key in kwargs:
            if key.lower().startswith('markertype'):
                mkt = kwargs[key]
            elif key.lower().startswith('markercolor'):
                mkc = kwargs[key]
            elif key.lower() == 'useerror':
                UseErr = kwargs[key]
            else:
                pass
        
        self.Points[Label] = {'dict':ParDict,\
                              'mkt':mkt,\
                              'mkc':mkc,\
                              'UseErr':UseErr,\
                              'File':FileName}
                              
    def generateAxisText(**kwargs):
        
        for key in kwargs:
            if key.lower() == 'parformat':
                self.parDict.update(kwargs[key])
            else:
                for par in self.parList:
                    self.parDict[par] =\
                    {'label':par,'axForm':None}
                    
    def generateAxisProperties(**kwargs):
        
        for key in kwargs:
            if key.lower() == 'axisform':
                self.parDict.update(kwargs[key])
            else:
                for par in self.parList:
                    self.parDict[par] =\
                    {'axisTicks':None,\
                     'axisRange':None}
                     
    def initPlots(self,**kwargs):
        
        UseHist = False
        bins = 15
        DataDict = {}
        for key in kwargs:
            if key.lower() == 'hist':
                UseHist = kwargs[key]
            if key.lower() == 'histbins':
                bins = kwargs[key]
            if key.lower() == 'data':
                DataDict = kwargs[key]
            else:
                for par in self.parList:
                    DataDict[par] = read1parMCMC(self.DataFile,par)
        
        HistX = {}
        for ix in range(self.GridNX):
            xName=[]
            ymax = 0
            for iy in range(self.GridNY):
                if not self.GridDict[(ix,iy)] == None:
                    #Get the x and y data for contour plot
                    par_x = self.GridDict[(ix,iy)][0]
                    par_y = self.GridDict[(ix,iy)][1]
                    d_x = DataDict[par_x]
                    d_y = DataDict[par_y]
                    PlotGrid[(ix,iy)] = singleJC(d_x,d_y)
                    xName.append(self.GridDict[(ix,iy)][0])
                    ymax =+ 1
                else:
                    PlotGrid[(ix,iy)] = None
            if len(list(set(xName))) > 1 and useHist:
                raise NameError("X parameters not same for histogram plot")
            elif len(list(set(xName))) == 0:
                raise NameError("X parameters not found MCMC plot")
            else:
                HistX.update({par_x:(ix,ymax+1)})
                
        print PlotGrid
        print HistX

        for par in self.parList:
            if UseHist:
                histPlot = hist(data[par], bins=bins)
            else:
                histPlot = None

            ParDict[par] = {'label':label,\
                            'axisTicks':axisTicks,\
                            'axisRange':rg}
                            
            PlotGrid[(ix,iy)] = histPlot