
import matplotlib
import sys
import numpy as np
import scipy
import scipy.ndimage
from matplotlib import pyplot as plt
from tmcmc.iopostmcmc import isNonParam, read1parMCMC, getPars
from tmcmc.iomcmc import ReadStartParams
from matplotlib import pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from matplotlib.font_manager import fontManager, FontProperties
import tmcmc

File = 'test1.mcmc'
par = ReadStartParams('FIT1.par')
#pars = getPars('MCMC4plot.mcmc')
pars = getPars(File)

#par1 = 'D.T1.T2.T3'
par1 = 'tT'
par2 = 'tG'

#for par in pars:
d1 = read1parMCMC(File,par1)
d2 = read1parMCMC(File,par2)

x = np.array(d1[par1])
y = np.array(d2[par2])

sigma_arr = np.array([1e0,2e0,3e0,4e0,5e0])
levels = scipy.special.erf(sigma_arr/np.sqrt(2e0))

hist2D,xedge,yedge = np.histogram2d(x,y,bins=(25,15))

hist2D = np.transpose(hist2D)
histlist = tmcmc.plotmcmc.return1Dfrom2D(hist2D)
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
xarr = tmcmc.plotmcmc.rangeMidpoints(x1)
yarr = tmcmc.plotmcmc.rangeMidpoints(y1)
#xarr = x1[1:]
#yarr = y1[1:]

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
smooth2D = hist2D #scipy.ndimage.filters.median_filter(hist2D,size=3)
#extent = [yedge[0],yedge[-1],xedge[-1],xedge[0]]
plt.subplot(3,1,1)
plt.plot(x,y,'k.')

CSV = plt.contourf(xarr,yarr,smooth2D,levels=newlev,colors=colortup)
CS = plt.contour(xarr,yarr,smooth2D,levels=newlev[:-1],colors='k')
#plt.clabel(CS,inline=1,fontsize=12,fmt=clevel)
plt.text(par[par1]['value'],par[par2]['value'],'+')
plt.xlabel(par1)
plt.ylabel(par2)
plt.xlim([min(x),max(x)])
plt.ylim([min(y),max(y)])
#for el_x in xedge:
    #for el_y in yedge:
        #plt.plot([-1,1],[el_y,el_y],'g-')
    #plt.plot([el_x,el_x],[-1,1],'g-')

plt.subplot(3,1,2)
plt.plot(x,'b.')
plt.text(len(x)/2e0,par[par1]['value'],'+')
plt.subplot(3,1,3)
plt.plot(y,'b.')
plt.text(len(y)/2e0,par[par2]['value'],'+')

plt.show()