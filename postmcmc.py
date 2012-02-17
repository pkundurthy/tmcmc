
import numpy as np
import scipy.stats
from iopostmcmc import readMCMChdr, read1parMCMC
from iopostmcmc import isNonParam
from matplotlib import pyplot as plt
import itertools
import sys
if sys.version_info[1] < 6:
    from tmcmc.misc import format
    
def covcorStats(File, FileTag, **kwargs):
    """ Given MCMC parameters, this function computes
        the covariance between parameters, the pearson's correlation 
        coefficient and spearman's rank correlation.
    """
    
    DFlag = False
    for key in kwargs:
        if key.lower().startswith('derive'):
            DFlag = kwargs[key]
    
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
                    d1 = read1parMCMC(File,key1,derived=DFlag)
                    d2 = read1parMCMC(File,key2,derived=DFlag)
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
    
def sortStats(StatDict, stype):
    

    keys = StatDict[stype].keys()
    comboList = []
    StatVal = []
    for combo in itertools.combinations(keys,2):
        value = abs(StatDict[stype][combo[0]][combo[1]]['value'])
        StatVal.append(value)
        comboList.append(combo)

    StatVal = np.array(StatVal)
    ind = StatVal.argsort()
    sortDict = {}
    j = 0
    for i in ind[::-1]:
        sortDict[j] = {'combo':comboList[i],'value':StatVal[i]}
        j += 1

    return sortDict

def plotChain(File1, **keywords):
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
                i1 = d1['istep']
                x1 = d1[key]
                pp = plt.plot(i1,x1,'b.')
                plt.title(key+' '+ftag)
                plt.savefig(ftag+'.TRACE.par'+key+'.png')
                if not silent: print 'plotting Trace for '+key
                plt.clf()
            except:
                print 'key not found'
                raise
    
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
            #print np.shape(data['istep'])
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

def GelmanRubinConvergence(FileList,ModelFile,OutFile, **kwargs):
    """The Gelman-Rubin convergence statistic. 
    When this is close to 1, the parameter chain has converged"""

    smallM = len(FileList)
    hdrKeys = readMCMChdr(FileList[0])
    GRFile = open(OutFile,'w')
    print >> GRFile, "# Gelman-Rubin Statistic per parameter"
    lastN = 0
    for keyw in kwargs:
        if keyw == 'lastn':
            lastN = kwargs[keyw]

    for i1 in hdrKeys.keys():
        key1 = hdrKeys[i1]
        if isNonParam(key1):
            pass
        else:
            xmean_vector = []
            si2_vector = []
            xi2_vector = []
            allX = []
            
            for iChain in range(smallM):
                dp = read1parMCMC(FileList[iChain],key1)
                x = dp[key1][-1*lastN:]
                if iChain == 0:
                    smallN = len(x)
                else:
                    alternateN = len(x)
                    if alternateN != smallN:
                        print 'Chain lengths are not the same for'
                        print FileList[0], ' and ', FileList[iChain]
                        print 'try using lastN keyword'
                        sys.exit()
                    
                xmean_vector.append(np.mean(x))
                si2_vector.append(np.var(x))
                xi2_vector.append(np.mean(x)**2)
                allX.extend(x)
                
            xmean_vector = np.array(xmean_vector)
            si2_vector = np.array(si2_vector)
            xi2_vector = np.array(xi2_vector)
            allX = np.array(allX)
            
            Bn = np.var(xmean_vector)
            W = np.mean(si2_vector)
            
            sig2hat = ((smallN-1)*W)/smallN + Bn
            Vhat = sig2hat + Bn/smallM
            
            term1 = (((smallN-1)/smallN)**2)*(1e0/smallM)*np.var(si2_vector)
            term2 = (((smallM + 1)/smallM)**2)*(2e0/(smallM-1))*(Bn**2)
            term3a = 2e0*((smallM + 1)*(smallN -1)/(smallM*(smallN**2)) )
            cov_si2_xi2 = np.cov( si2_vector, xi2_vector) 
            cov_si2_x = np.cov(si2_vector, xmean_vector)
            xdash = np.mean(allX)
            term3b = (smallN/smallM)*(cov_si2_xi2[0][1] - 2e0*xdash*cov_si2_x[0][1])
            
            varVhat = term1 + term2 + term3a*term3b
            df = 2e0*(Vhat**2)/(varVhat)
            Rhat = (Vhat/W)*(df/(df-2e0))
            print key1, Rhat
            print >> GRFile, key1+' = ',Rhat

    GRFile.close()