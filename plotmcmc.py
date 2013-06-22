import sys
if sys.version_info[1] < 6:
    from tmcmc.misc import format
import numpy as np
import scipy
import scipy.ndimage
from iopostmcmc import isNonParam, read1parMCMC, getPars
from iomcmc import ReadStartParams, checkFileExists
from binning import MedianMeanOutlierRejection
from matplotlib import rc
rc('text',usetex=True)
rc('font',family='serif')
import matplotlib.colors
from matplotlib import pyplot as plt
from matplotlib.ticker import FormatStrFormatter,MaxNLocator, FixedLocator
from matplotlib.font_manager import fontManager, FontProperties
#from matplotlib.gridspec import GridSpec

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
            
    return JC(par1,par2,new_data)

def JC(par1,par2,dataMCMC):
    """ make a single Joint-Correlation plot """
    
    x = np.array(dataMCMC[par1])
    y = np.array(dataMCMC[par2])
    mm1, sdv1, ngood1, goodindex1, badindex1 = \
    MedianMeanOutlierRejection(x,5,'median')
    x = x[goodindex1]
    y = y[goodindex1]

    #sigma_arr = np.array([1e0,2e0,3e0,4e0,5e0])
    sigma_arr = np.array([1e0,3e0,5e0])
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
    
    #cmap = matplotlib.colors.Colormap('jet',N=5)
    cmap = matplotlib.colors.Colormap('jet',N=3)
    #sig_labels = (r'1-$\sigma$',r'2-$\sigma$',r'3-$\sigma$',r'4-$\sigma$',r'5-$\sigma$')
    sig_labels = (r'1-$\sigma$',r'3-$\sigma$',r'5-$\sigma$')
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
    #colortup = ('#FF6600','#FF9900','#FFCC00','#FFFF00','#FFFF99')
    colortup = ('#FF6600','#FFCC00','#FFFF99')
    smooth2D = hist2D #scipy.ndimage.filters.median_filter(hist2D,size=3)
    #extent = [yedge[0],yedge[-1],xedge[-1],xedge[0]]
    CSV = plt.contourf(xarr,yarr,smooth2D,levels=newlev,colors=colortup)
    CS = plt.contour(xarr,yarr,smooth2D,levels=newlev[:-1],colors='k')
    plt.clabel(CS,inline=1,fontsize=12,fmt=clevel)
    #cb = plt.colorbar(CSV)
    return plt.figure
    
def getRange(d,**kwargs):
    
    # default
    ext0 = 0
    ext1 = 0
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

def subID(Coord,Nx,Ny):
    """ Returns subplot ID number given x,y
    grid coordinates for a x= left-to-right, y=top-to-bottom 
    coordinate system.
    """
    
    x = Coord[0]
    y = Coord[1]
    
    plotID = (x+1) + (Ny-1-y)*Nx
    
    return plotID

def SimplifyGrid(xp,yp):
    """
    Given two lists of parameters, this function outputs
    the "best" possible grid configuration for triplot.
    xp and yp are expected to go from left-to-right and
    top-to-bottom respectively.
    """
    
    xpD = {}
    ypD = {}
    for i in range(len(xp)):
        xpD[i] = xp[i]
    for i in range(len(yp)):
        ypD[i] = yp[i]
    #xp = sorted(xp)
    #yp = sorted(yp)
    GridDict = {}
    for ix in xpD.keys():
    #for ix in range(len(xp)):
        go = True
        #for iy in range(len(yp)):
        for iy in ypD.keys():
            if xpD[ix] == ypD[iy]:
                go = False
            if go:
                #print ix,iy, xpD[ix], ypD[iy]
                GridDict[(ix,iy)] = (xpD[ix],ypD[iy])

    return GridDict

class triplot:

    def __init__(self,GridDict,MCMCFileList,xp,yp):

        maxY = 0
        maxX = 0
        for Grid in GridDict.keys():
            if Grid[0] > maxX:
                maxX = Grid[0]
            if Grid[1] > maxY:
                maxY = Grid[1]

        self.GridNX = maxX+1
        self.GridNY = maxY+1
        parList = []
        for ix in range(self.GridNX):
            for iy in range(self.GridNY):
                try:
                    parList.append(GridDict[(ix,iy)][0])
                    parList.append(GridDict[(ix,iy)][1])
                except:
                    GridDict[(ix,iy)] = None

        self.parList = list(set(parList))
        self.GridDict = GridDict
        if type(MCMCFileList) is list:
            self.DataFile = MCMCFileList
        else:
            self.DataFile = [MCMCFileList]
        self.xpars = xp
        self.ypars = yp
        self.parDict = {}
        for par in parList:
            self.parDict[par] = {'label':par,\
                                 'axForm':None,\
                                 'axisTicks':None,\
                                 'axisRange':None}

    def addFits(self,Label,params,**kwargs):

        mkt = 'o'
        mkc = 'r'
        UseErr = False
        try:
            dummy = self.Fits
        except:
            self.Fits = {}

        for key in kwargs:
            if key.lower().startswith('markertype'):
                mkt = kwargs[key]
            elif key.lower().startswith('markercolor'):
                mkc = kwargs[key]
            elif key.lower() == 'useerror':
                UseErr = kwargs[key]
            else:
                pass

        self.Fits[Label] = {'dict':params,\
                            'mkt':mkt,\
                            'mkc':mkc,\
                            'UseErr':UseErr}

    def generateAxisText(self,**kwargs):

        for key in kwargs:
            if key.lower() == 'parformat':
                for par in self.parList:
                    self.parDict[par].update(kwargs[key][par])
            else:
                pass

    def generateAxisProperties(self,**kwargs):

        for key in kwargs:
            if key.lower() == 'axisform':
                for par in self.parList:
                    self.parDict[par].update(kwargs[key][par])
            else:
                pass

    def initPlots(self,**kwargs):

        UseHist = False
        hbins = 25
        DataDict = {}
        for par in self.parList:
            for dFile in self.DataFile:
                try:
                    DataDict[par] = read1parMCMC(dFile,par)[par]
                except:
                    pass

        for key in kwargs:
            if key.lower() == 'hist':
                UseHist = kwargs[key]
            if key.lower() == 'binhist':
                hbins = long(kwargs[key])
            if key.lower() == 'data':
                DataDict = kwargs[key]

        self.hbins = hbins
        self.UseHist = UseHist
        self.DataDict = DataDict

        if self.UseHist:
            self.GridNX += 1
            self.GridNY += 1

        HistDict = {}
        for par in self.parList:
            ix = None
            iy = None
            try:
                xid = self.xpars.index(par)
            except:
                xid = None
            try:
                yid = self.ypars.index(par)
            except:
                yid = None
            if xid != None:
                ix = xid
                iy = self.GridNY-xid-1
                Or = 'vertical'
            else:
                ix = self.GridNX-1
                iy = 0
                Or = 'horizontal'
            if UseHist:
                HistDict[(ix,iy)] = (par,Or)
            else:
                HistDict[(ix,iy)] = None

        self.HistDict = HistDict

    def addTitle(self,x,y, TitleString):
        
        self.xTitleStr = x
        self.yTitleStr = y
        self.TitleString = TitleString
        
    def addWarning(self,WarningString):
        self.WarningString = WarningString 

    def makePlot(self, **kwargs):

        PlotFile = False
        fSzX = 16
        fSzY = 16
        legfsz = 16
        loctup=(self.GridNX-1,self.GridNY)
        for key in kwargs:
            if key.lower().startswith('plotfile'):
                PlotFile = True
                FileName = kwargs[key]
            if key.lower().startswith('fsizex'):
                fSzX = long(kwargs[key])
            if key.lower().startswith('fsizey'):
                fSzY = long(kwargs[key])
            if key.lower().startswith('legfontsz'):
                legfsz = long(kwargs[key])
            if key.lower().startswith('legloc'):
                loctup = kwargs[key]

        width, height = matplotlib.rcParams['figure.figsize']
        size = min( [width,height])
        # make a square figure
        fig = plt.figure(figsize=(size,size))

        leglab = {}
        legFontSz = 12
        if len(self.Fits.keys()) > 2: 
            legFontSz = 10

        LegFont = FontProperties(size=legFontSz)
        for Grid in self.GridDict.keys():
            LegMade = False
            if self.GridDict[Grid] != None:
                par_x = self.GridDict[Grid][0]
                par_y = self.GridDict[Grid][1]
                d_x = {par_x:self.DataDict[par_x]}
                d_y = {par_y:self.DataDict[par_y]}
                plotID = subID(Grid,self.GridNX,self.GridNY)
                plt.subplot(self.GridNX,self.GridNY,plotID)
                singleJC(d_x,d_y)
                #plot Fits if added:
                if hasattr(self,'Fits'):
                    for key in self.Fits.keys():
                        parXExists = False
                        parYExists = False
                        if par_x in self.Fits[key]['dict'].keys():
                            parXExists = True
                            xarr = [-9e3,self.Fits[key]['dict'][par_x]['value']]
                        if par_y in self.Fits[key]['dict'].keys():
                            parYExists = True
                            yarr = [-9e3,self.Fits[key]['dict'][par_y]['value']]

                        if parXExists and parYExists:
                            if isinstance(self.Fits[key]['dict'][par_x]['step'],list):
                                xerrArr0 = [0,self.Fits[key]['dict'][par_x]['step'][0]]
                                xerrArr1 = [0,self.Fits[key]['dict'][par_x]['step'][1]]
                                yerrArr0 = [0,self.Fits[key]['dict'][par_y]['step'][0]]
                                yerrArr1 = [0,self.Fits[key]['dict'][par_y]['step'][1]]
                                xerrArr = [xerrArr0,xerrArr1]
                                yerrArr = [yerrArr0,yerrArr1]
                                #print xerrArr
                                #print yerrArr
                            else:
                                xerrArr = [0,self.Fits[key]['dict'][par_x]['step']]
                                yerrArr = [0,self.Fits[key]['dict'][par_y]['step']]

                            mkt = self.Fits[key]['mkt']
                            mkc = self.Fits[key]['mkc']
                            #print key, self.Fits.keys(), par_x, par_y, leglab
                            mark = plt.plot(xarr,yarr,marker=mkt,markerfacecolor=mkc,linestyle='None')
                            if self.Fits[key]['UseErr']:
                                plt.errorbar(xarr,yarr,xerr=xerrArr,\
                                            yerr=yerrArr,fmt=None,\
                                            marker=mkt,ecolor=mkc)
                            if not LegMade:
                                leglab[key] = mark
                                #leglab.append(key)
                                #legmark.append(mark)

                #Axis Formatting
                plt.xlim(self.parDict[par_x]['axisRange'])
                plt.ylim(self.parDict[par_y]['axisRange'])
                if self.parDict[par_x]['axisTicks'] != None:
                    plt.setp(plt.gca(),\
                         xticks=self.parDict[par_x]['axisTicks'])
                if self.parDict[par_y]['axisTicks'] != None:
                    plt.setp(plt.gca(),\
                         yticks=self.parDict[par_y]['axisTicks'])
                if Grid[1] == 0:
                    plt.xlabel(self.parDict[par_x]['label'],\
                               fontsize=fSzX)
                    if self.parDict[par_x]['axForm'] != None:
                        plt.setp(plt.gca().xaxis.set_major_formatter(self.parDict[par_x]['axForm']))
                else:
                    plt.setp(plt.gca(),xticklabels=[])
                if Grid[0] == 0:
                    plt.ylabel(self.parDict[par_y]['label'],\
                               fontsize=fSzY)
                    if self.parDict[par_y]['axForm'] != None:
                        plt.setp(plt.gca().yaxis.set_major_formatter(self.parDict[par_y]['axForm']))
                else:
                    plt.setp(plt.gca(),yticklabels=[])
        
        if hasattr(self,'Fits'):
            plotID = subID((0,0),self.GridNX,self.GridNY)
            plt.subplot(self.GridNX,self.GridNY,plotID)
            plt.legend(tuple(leglab.values()),\
                       tuple(leglab.keys()),\
                       numpoints=1,\
                       loc='upper left',\
                       prop=LegFont,\
                       bbox_to_anchor=loctup)

        #check for Histogram plotting
        if self.UseHist:
            for Grid in self.HistDict.keys():
                if self.HistDict[Grid] != None:
                    par = self.HistDict[Grid][0]
                    ori = self.HistDict[Grid][1]
                    d = {par:self.DataDict[par]}
                    plotID = subID(Grid,self.GridNX,self.GridNY)
                    #print plotID, Grid
                    plt.subplot(self.GridNX,self.GridNY,plotID)
                    plt.hist(d[par],bins=self.hbins,orientation=ori,\
                             histtype='step',color='black')
                    tickForm = FormatStrFormatter('%.2e')
                    if ori.startswith('vert'):
                        plt.setp(plt.gca(),xticklabels=[])
                        plt.setp(plt.gca().yaxis.set_major_formatter(tickForm))
                        tickLoc = MaxNLocator(nbins=4,prune='both')
                        plt.setp(plt.gca().yaxis.set_major_locator(tickLoc))
                        plt.ylabel(r'Number')
                        for tick in plt.gca().yaxis.get_major_ticks():
                            if Grid[0] == 0:
                                tick.label1On = True
                                tick.label2On = False
                            else:
                                tick.label1On = False
                                tick.label2On = True
                                plt.gca().yaxis.set_label_position('right')
                        plt.xlim(self.parDict[par]['axisRange'])
                    else:
                        plt.setp(plt.gca().xaxis.set_major_formatter(tickForm))
                        tickLoc = MaxNLocator(nbins=2,prune='both')
                        plt.setp(plt.gca().xaxis.set_major_locator(tickLoc))
                        plt.setp(plt.gca(),yticklabels=[])
                        plt.xlabel(r'Number')
                        for tick in plt.gca().xaxis.get_major_ticks():
                            if Grid[1] == 0:
                                tick.label1On = True
                                tick.label2On = False
                            else:
                                tick.label1On = False
                                tick.label2On = True
                        plt.ylim(self.parDict[par]['axisRange'])

        plt.subplots_adjust(hspace=0)
        plt.subplots_adjust(wspace=0)

        if hasattr(self, 'TitleString'):
            print self.TitleString, size
            plt.figtext(self.xTitleStr,\
                        self.yTitleStr,self.TitleString,\
                        fontsize=fSzY)
        if hasattr(self, 'WarningString'):
            fdict = {'family' : 'monospace','color':'b'}
            plt.figtext(0.5,0.5,self.WarningString,fontsize=24,rotation=45, **fdict)

        if PlotFile:
            plt.savefig(FileName,bbox_inches='tight',pad_inches=0.5)
            #plt.savefig(FileName,bbox_inches='tight')
            #plt.savefig(FileName,pad_inches=0.5)
        else:
            plt.show()

class statTriplot:
    
    def __init__(self, xpars,ypars):
        
        self.xp = xpars
        self.yp = ypars
        
        self.GridDict = SimplifyGrid(self.xp,self.yp)
        #for key in self.GridDict.keys():
            #print key, self.GridDict[key]
        
        maxX = 0
        maxY = 0
        for Grid in self.GridDict.keys():
            if Grid[0] > maxX:
                maxX = Grid[0]
            if Grid[1] > maxY:
                maxY = Grid[1]

        self.GridNX = maxX+1
        self.GridNY = maxY+1

    def parText(self,parLabel):

        Label = {}
        for grid in self.GridDict.keys():
            Label[grid] = {'x':parLabel[self.GridDict[grid][0]]['label'],\
                           'y':parLabel[self.GridDict[grid][1]]['label']}

        self.Label = Label

    def statsTable(self,Stats,stype, **kwargs):

        width, height = matplotlib.rcParams['figure.figsize']
        size = max([width,height])
        # make a square figure
        fig = plt.figure(figsize=(size,size))

        # default font sizes
        xfsize = np.floor(300e0*size/(24*max(self.GridNX,self.GridNY)))
        yfsize = np.floor(300e0*size/(24*max(self.GridNX,self.GridNY)))
        fsize = np.floor(300e0*size/(24*max(self.GridNX,self.GridNY)))
        yshift = 0
        xshift = 0
        PlotFile = False
        TitleString = ''
        #print xfsize,yfsize,fsize
        if fsize > 24.0:
            fsize = 24.0
        if xfsize > 18.0:
            xfsize = 18.0
        if yfsize > 18.0:
            yfsize = 18.0
            
        for key in kwargs:
            if key.lower().startswith('plotfile'):
                PlotFile = True
                FileName = kwargs[key]
            elif key.lower().startswith('numfsize'):
                fsize = kwargs[key]
            elif key.lower().startswith('fsizex'):
                xfsize = kwargs[key]
            elif key.lower().startswith('fsizey'):
                yfsize = kwargs[key]
            elif key.lower().startswith('xshift'):
                xshift = kwargs[key]
            elif key.lower().startswith('yshift'):
                yshift = kwargs[key]
            elif key.lower().startswith('title'):
                TitleString = kwargs[key]
            else:
                pass

        for grid in self.GridDict.keys():
            plotID = subID(grid,self.GridNX,self.GridNY)
            plt.subplot(self.GridNY,self.GridNX,plotID)

            Stat = Stats[stype]\
                        [self.GridDict[grid][0]]\
                        [self.GridDict[grid][1]]\
                        ['value']

            absStat = abs(Stat)

            cross = np.linspace(0,1,3)
            plt.plot(cross,cross,marker='o',\
                     markerfacecolor='w',\
                     markeredgecolor='w',\
                     linestyle='None')
            #numsplit = map(str,text.split('e'))
            #OutText = r'%s$\times 10^{%s}$' % (numsplit[0],numsplit[1])
            if absStat < 0.01:
                text = r'$< 0.01$'
                OutText = r'%s' % text
                plt.text(0.0-xshift,0.4-yshift,OutText,fontsize=fsize)
            elif absStat >= 0.5:
                text = format(abs(Stat),'0.2f')
                plt.subplot(self.GridNY,self.GridNX,plotID, axisbg='gray')
                OutText = r'%s' % text
                plt.text(0.0-xshift,0.4-yshift,OutText,fontsize=fsize,color='w')
            else:
                text = format(abs(Stat),'0.2f')
                plt.subplot(self.GridNY,self.GridNX,plotID)
                OutText = r'%s' % text
                plt.text(0.0-xshift,0.4-yshift,OutText,fontsize=fsize)

            plt.setp(plt.gca(),yticklabels=[],yticks=[])
            plt.setp(plt.gca(),xticklabels=[],xticks=[])
            if grid[1] == 0:
                #print self.Label[grid]['x'], grid
                plt.xlabel(self.Label[grid]['x'],fontsize=xfsize)
            if grid[0] == 0:
                #print self.Label[grid]['y'], grid
                plt.ylabel(self.Label[grid]['y'],fontsize=yfsize)
            
        plt.subplots_adjust(hspace=0)
        plt.subplots_adjust(wspace=0)
        plt.suptitle(TitleString,fontsize=24,y=0.95)

        if PlotFile:
            plt.savefig(FileName,pad_inches=0.5)
        else:
            plt.show()
