""" Contains various functions needed for the lightcurve binning process. """

import numpy as np
import sys
if sys.version_info[1] < 6:
    from tmcmc.misc import format

def MedianMeanOutlierRejection(indata, cutoff, choice):
    """ Computes an outlier rejected mean or median of a data array.
    Based on the robust median, and mean calculator robustmm.
    Inputs
        indata - numpy data array
        cutoff - number, such as 3,4 or 5 sigma clipping values
        choice - return 'MEDIAN' or 'MEAN'
    """

    indata = np.array(indata)
    med = np.median(indata.ravel())
    absdev = abs(indata-med)
    medabsdev = np.median(absdev)

    # check if cutoff is too small
    if cutoff < 1.0:
        #print 'Warning: Truncation might remove useful points. Setting cutoff to 1-sigma.'
        cutoff = 1.0
    else:
        cutoff = cutoff
    
    sc = cutoff*medabsdev/0.6745e0
    goodindex = np.where(absdev <= sc)[0]
    badindex = np.where(absdev > sc)[0]

    # compute mean or median, median is recommended
    if choice.upper() == 'MEAN':
        mm = np.mean(indata[goodindex])
    if choice.upper() == 'MEDIAN':
        mm = np.median(indata[goodindex])
    sdv = np.std(indata[goodindex])
    ngood = len(goodindex)
        
    return mm, sdv, ngood, goodindex, badindex

def makeGridRange(x0,xEnd,bin):
    """ Given the first and last elements of a sorted list, 
    this routine places a grid with the interval = bin around the data.
    Inputs
        x0 - lowest value of the array
        xEnd - highest value of the array
        bin - size of bin to make the grid
    Output
        tuplerange = a dictionary with the grid low and high points
        {0:(0.3,0.4),1:(0.4,0.5),3:(0.5,0.6)...} 
    """
    
    # make tuple with low and high stored as a tuple within
    # a dictionary. with dict keys being the bin number
    x = x0 + bin
    tuplerange = {0:(x0,x)}
    i = 1
    while x <= xEnd:
        tuplerange[i] = (x,x+bin)
        i += 1
        x = x + bin

    return tuplerange

def isInRange(x,x0,x1):
    """ Check if element is in a given range. 
    range = x0 - x1
    element = x
    """
    
    if x >= x0 and x < x1:
        return True
    else:
        return False

def GridBinning(x,y,yerr,bin):
    """ Bin x, y and yerr within a grid on x with interval = bin.
     Inputs
        x - abscissa of data
        y - ordinate of data
        yerr - error in ordinate values
        bin - the bin size by which to lump the abscissa
    Output
        Five numpy arrays with binned data
        xout, yout, yerrout, yerrmeanout, npoints
        xout - binned abscissa
        yout - binned ordinate
        yerrout - binned errors in ordinate
        yerrmeanout - errors in the mean for the binned ordinate
        npoints - number of points in each bin
    """

    dict = {}
    for i in range(len(x)):
        dict[x[i]] = {'index':i,'y':y[i],'yerr':yerr[i]}

    x = np.array(x)
    y = np.array(y)
    yerr = np.array(yerr)

    x0 = min(dict.keys())
    xEnd = max(dict.keys())
    nleft = len(x)
    # print x0, xEnd, bin
    grid = makeGridRange(x0,xEnd,bin)
    
    # create empty arrays of output lists
    xout = []
    yout = []
    yerrout = []
    yerrmeanout = []
    npoints = []
    print 'Grid size =',len(grid), 'Bin size = ',bin
    it = 0
    for key in grid.keys():
        condition = []
        it += 1
        for el in sorted(dict.keys()):
            condition.append(isInRange(el,grid[key][0],grid[key][1]))
        condition = np.array(condition)
        if len(y[condition]) > 1:
            xout.append(0.5*(grid[key][0]+grid[key][1]))
            yout.append(np.mean(y[condition]))
            yerrout.append(np.sqrt(np.sum(yerr[condition]**2))/len(y[condition]) )
            yerrmeanout.append(np.std(y[condition])/np.sqrt(len(y[condition])))
            npoints.append(len(y[condition]))

    return np.array(xout), np.array(yout), np.array(yerrout), np.array(yerrmeanout), np.array(npoints)