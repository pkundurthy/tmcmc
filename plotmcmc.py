


def cmap_map(function,cmap):
    """ Applies function (which should operate on vectors of shape 3:
    [r, g, b], on colormap cmap. This routine will break any discontinuous     points in a colormap.
    """
    cdict = cmap._segmentdata
    step_dict = {}
    # Firt get the list of points where the segments start or end
    for key in ('red','green','blue'):         step_dict[key] = map(lambda x: x[0], cdict[key])
    step_list = sum(step_dict.values(), [])
    step_list = np.array(list(set(step_list)))
    # Then compute the LUT, and apply the function to the LUT
    reduced_cmap = lambda step : np.array(cmap(step)[0:3])
    old_LUT = np.array(map( reduced_cmap, step_list))
    new_LUT = np.array(map( function, old_LUT))
    # Now try to make a minimal segment definition of the new LUT
    cdict = {}
    for i,key in enumerate(('red','green','blue')):
        this_cdict = {}
        for j,step in enumerate(step_list):
            if step in step_dict[key]:
                this_cdict[step] = new_LUT[j,i]
            elif new_LUT[j,i]!=old_LUT[j,i]:
                this_cdict[step] = new_LUT[j,i]
        colorvector=  map(lambda x: x + (x[1], ), this_cdict.items())
        colorvector.sort()
        cdict[key] = colorvector

    return matplotlib.colors.LinearSegmentedColormap('colormap',cdict,1024)

def rangeMidpoints(x):
    """         """
    
    newx = []
    for i in range(len(x)-1):
        newx.append(0.5e0*(x[i]+x[i+1]))

    return np.array(newx)

def return1Dfrom2D(arr2D):
    
    arr1D = []
    shape = arr2D.shape
    #print arr2D.shape
    for j in range(shape[0]):
        for i in range(shape[1]):
            arr1D.append(arr2D[i,j])
    
    return arr1D

def singleJC1data(data1,data2):
    """ make a single Joint-Correlation plot from single parameter dictionaries """
    
    new_data = {}
    for key in data1.keys():
        if key != 'chi1' and key != 'istep':
            par1 = key
            new_data[par1] = data1[par1]
    for key in data2.keys():
        if key != 'chi1' and key != 'istep':
            par2 = key    
            new_data[par2] = data2[par2]
            
    singleJC(par1,par2,new_data)

def singleJC(par1,par2,dataMCMC):
    """ make a single Joint-Correlation plot """
    
    x = np.array(dataMCMC[par1])
    y = np.array(dataMCMC[par2])
    #xmin = np.min(x)
    #xmax = np.max(x)
    #ymin = np.min(y)
    #ymax = np.max(y)
    #print x.size, y.size
    sigma_arr = np.array([1e0,2e0,3e0,4e0,5e0])
    levels = scipy.special.erf(sigma_arr/np.sqrt(2e0))
    
    hist2D,xedge,yedge = np.histogram2d(x,y,bins=25)
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
    
    clev = [x for x in levelID if x not in locals()['_[1]']]
    #print clev
    x1 = np.array(xedge.tolist())
    y1 = np.array(yedge.tolist())
    xarr = rangeMidpoints(x1)
    yarr = rangeMidpoints(y1)
    
    #cmap = cmap_map(lambda x: x**(0.5)+0.5, plt.cm.jet)
    cmap = matplotlib.colors.Colormap('jet',N=5)
    sig_labels = (r'1-$\sigma$',r'2-$\sigma$',r'3-$\sigma$',r'4-$\sigma$',r'5-$\sigma$')
    sig_labels = sig_labels[::-1]
    clevel = {}
    newlev = []
    for i in range(len(sig_labels)):
        clevel[clev[i]] = sig_labels[i]
        newlev.append(clev[i])
    clevel[0] = ''
    #newlevalt = newlev.copy()
    newlev.append(0)
    #colortup = ('#99CC00','#99CC33','#99CC66','#99CC99','#99CCCC','#99CCFF')
    #colortup = ('#339900','#66CC00','#99FF33','#CCCC99','#FFFF99')
    colortup = ('#FF6600','#FF9900','#FFCC00','#FFFF00','#FFFF99')
    #print newlev, newlevalt
    #print clevel
    smooth2D = scipy.ndimage.filters.median_filter(hist2D,size=3)
    CSV = plt.contourf(xarr,yarr,smooth2D,levels=newlev,colors=colortup)
    CS = plt.contour(xarr,yarr,smooth2D,levels=newlev[:-1],colors='k')
    plt.xlabel(par1)
    plt.ylabel(par2)
    plt.clabel(CS,inline=1,fontsize=12,fmt=clevel)
    cb = plt.colorbar(CSV)
    cb.ax.set_yticklabels(sig_labels)
    plt.show()