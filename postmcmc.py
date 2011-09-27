
import numpy as np
import scipy.stats
from iopostmcmc import readMCMChdr, read1parMCMC
from iopostmcmc import isNonParam
from matplotlib import pyplot as plt
import sys

def covcorStats(File, FileTag):
    """ Given MCMC parameters, this function computes
        the covariance between parameters, the pearson's correlation 
        coefficient and spearman's rank correlation.
    """
    
    stats = {}
    OutFileObject_COV = open(FileTag+'_COV.data','w')
    OutFileObject_PR = open(FileTag+'_PEARSONSR.data','w')
    OutFileObject_SR = open(FileTag+'_SPEARMANSR.data','w')
    #print >> OutFileObject, '#  par1   |  par2   |  cov   | pearson\'s r  | spearman\'s r '
    topline = '#'
    passCount = 0
    hdrKeys1 = readMCMChdr(File)
    hdrKeys2 = readMCMChdr(File)
    
    for i1 in hdrKeys1.keys():
        key1 = hdrKeys1[i1]
        if isNonParam(key1):
            pass
        else:
            covline = ''
            pcorline = ''
            scorline = ''
            for i2 in hdrKeys2.keys():
                key2 = hdrKeys2[i2]
                if isNonParam(key2):
                    pass
                else:
                    d1 = read1parMCMC(File,key1)
                    d2 = read1parMCMC(File,key2)
                    if passCount == 0: topline = topline+5*' '+key2
                    cov = np.cov(d1[key1],d2[key2])
                    pcor = scipy.stats.pearsonr(np.array(d1[key1]),np.array(d2[key2]))
                    scor = scipy.stats.spearmanr(np.array(d1[key1]),np.array(d2[key2]))
                    print key1, key2
                    covline = covline+' '+format(cov[0][1],'+.2e')
                    pcorline = pcorline+' '+format(pcor[0],'+.2e')
                    scorline = scorline+' '+format(scor[0],'+.2e')
            if passCount == 0:
                print >> OutFileObject_COV, topline
                print >> OutFileObject_COV, '#'+88*'-'
                print >> OutFileObject_PR, topline
                print >> OutFileObject_PR, '#'+88*'-'
                print >> OutFileObject_SR, topline
                print >> OutFileObject_SR, '#'+88*'-'
            lenkey = len(key1)
            if lenkey < 10:
                fac = 10-lenkey
            else:
                fac = 10
            print >> OutFileObject_COV, key1+fac*' '+' | '+covline
            print >> OutFileObject_PR, key1+fac*' '+' | '+pcorline
            print >> OutFileObject_SR, key1+fac*' '+' | '+scorline
            passCount += 1
    
    OutFileObject_COV.close()
    OutFileObject_PR.close()
    OutFileObject_SR.close()
    
def plotTrace(File1,File2, **keywords):
    """ Plot the trace of a single parameter between two chains """
    
    #ftag = ''
    ftag = 'mcmc'
    silent = False
    for keyw in keywords:
        if keyw == 'ftag':
            ftag = keywords[keyw]
        if keyw == 'Silent':
            silent = keywords[keyw]
            
    hdrKeys = readMCMChdr(File1)

    for i in hdrKeys.keys():
        key = hdrKeys[i]
        if isNonParam(key):
            pass
        else:
            try:
                d1 = read1parMCMC(File1,key)
                d2 = read1parMCMC(File2,key)
                i1 = d1['istep']
                i2 = d2['istep']
                x1 = d1[key]
                x2 = d2[key]
                pp = plt.plot(i1,x1,'bo')
                plt.setp(pp,'markersize',8)
                plt.setp(pp,'markerfacecolor','k')
                pp = plt.plot(i2,x2,'r.')
                plt.savefig(ftag+'.TRACE.par'+key+'.png')
                if not silent: print 'plotting Trace for '+key
                plt.clf()
            except:
                print 'key not found'
                raise

def autocorMCMC(File, lowtol, jmax, OutStatFile, mkPlotsFlag, **keywords):
    """ Compute the auto-correlation of parameters in a chain """
    
    #ftag = ''
    ftag = 'mcmc'
    silent = False
    for keyw in keywords:
        if keyw == 'ftag':
            ftag = keywords[keyw]
        if keyw == 'Silent':
            silent = keywords[keyw]
    
    chain_stats = {}
    OutFileObject = open(OutStatFile,'w')
    hdrKeys = readMCMChdr(File)
    for i in hdrKeys.keys():
        key = hdrKeys[i]
        # empty list for autocorrelation data
        x = []
        # skip the non-parameter data
        if isNonParam(key):
            pass
        else:
            data = read1parMCMC(File,key)
            ChainLength = len(data['istep'])
            if not silent: print 'Par '+key
            for i in range(ChainLength):
                x.append(data[key][i])
            median_x = np.median(x)
            # removing median value
            x1 = np.array(x)-median_x
            cj = []                    # auto-correlation
            jarr = []                  # lag
            # starting auto-correlation, set to be much higher than tolerance
            cval = 1e0
            j = 0
            szx1 = len(x1)
            while cval > lowtol and j < jmax:
                sli0 = 0 
                sli1 = szx1-j-1
                slj0 = j
                slj1 = szx1-1
                next2 = x1[sli0:sli1]
                x1i_x1ipj = x1[sli0:sli1]*x1[slj0:slj1]
                x1i_sq = (x1[sli0:sli1]*x1[sli0:sli1])
                x1i = (x1[sli0:sli1])
                val = (np.mean(x1i_x1ipj) - (np.mean(x1i))**2)/\
                (np.mean(x1i_sq) - (np.mean(x1i))**2)
                cj.append(val)
                jarr.append(j)
                cval = val
                j += 1
            cj = np.array(cj)
            jarr = np.array(jarr)
            corlen_index = np.where( np.abs(cj-0.5e0) == np.min( np.abs(cj-0.5e0)) )[0]
            corlen = jarr[corlen_index[0]]
            efflen = long(float(ChainLength)/float(corlen))
            if mkPlotsFlag:
                print 'plotting acor', key
                plt.plot(jarr,cj,'b.')
                plt.plot([corlen,corlen],[0,1],'k--')
                plt.plot([0,max(jarr)],[0.5,0.5],'k--')
                plt.xlabel('j (Lag)')
                plt.ylabel('C (Auto-Correlation)')
                plt.title(ftag+' Auto-Correlation for "'+key+'"')
                plt.savefig(ftag+'.ACOR.par'+key+'.png')
                plt.clf()

            print >> OutFileObject, '##'+key+'## Corr Length = '+format(corlen,'d')
            print >> OutFileObject, '##'+key+'## Eff Length = '+format(efflen,'d')
            chain_stats[key] = {'corlength':corlen,'efflength':efflen}
    
    clen = []
    elen = []
    for key in chain_stats.keys():
        clen.append(chain_stats[key]['corlength'])
        elen.append(chain_stats[key]['efflength'])
    if not silent:
        print '## ALL ## Chain Length = '+format(ChainLength,'d')
        print '## ALL ## Corr Length = '+format(max(clen),'d')
        print '## ALL ## Eff Length = '+format(min(elen),'d')
    print >> OutFileObject, '## ALL ## Chain Length = '+format(ChainLength,'d')
    print >> OutFileObject, '## ALL ## Corr Length = '+format(max(clen),'d')
    print >> OutFileObject, '## ALL ## Eff Length = '+format(min(elen),'d')
    OutFileObject.close()
