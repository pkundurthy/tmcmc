
import numpy as np

def getNparams(hdrkeys):
    """ reports the number of model parameters in the MCMC file """
    
    Nparam = 0
    for key in hdrkeys.keys():
        if isNonParam(key):
            pass
        else:
            Nparam += 1
            
    return Nparam

def covcorStats(data, FileTag):
    """
        Given MCMC parameters, this function computes
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
    for key in data.keys():
        if isNonParam(key):
            pass
        else:
            covline = ''
            pcorline = ''
            scorline = ''
            for key2 in data.keys():
                if isNonParam(key2):
                    pass
                else:
                    if passCount == 0: topline = topline+5*' '+key2
                    cov = np.cov(data[key],data[key2])
                    pcor = scipy.stats.pearsonr(np.array(data[key]),np.array(data[key2]))
                    scor = scipy.stats.spearmanr(np.array(data[key]),np.array(data[key2]))
                    print key, key2
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
            lenkey = len(key)
            if lenkey < 10:
                fac = 10-lenkey
            print >> OutFileObject_COV, key+fac*' '+' | '+covline
            print >> OutFileObject_PR, key+fac*' '+' | '+pcorline
            print >> OutFileObject_SR, key+fac*' '+' | '+scorline
            passCount += 1
    
    OutFileObject_COV.close()
    OutFileObject_PR.close()
    OutFileObject_SR.close()
    
def plotTrace(data1, data2, **keywords):
    """ Plot the trace of a single parameter between two chains """
    
    #ftag = ''
    ftag = 'mcmc'
    silent = False
    for keyw in keywords:
        if keyw == 'ftag':
            ftag = keywords[keyw]
        if keyw == 'Silent':
            silent = keywords[keyw]

    for key in data1.keys():
        if isNonParam(key):
            pass
        else:
            try:
                i1 = data1['istep']
                i2 = data2['istep']
                x1 = data1[key]
                x2 = data2[key]
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

def autocorMCMC(data, lowtol, jmax, OutStatFile, mkPlotsFlag, **keywords):
    """ Compute the auto-correlation of parameters in a chain """
    
    #ftag = ''
    ftag = 'mcmc'
    silent = False
    for keyw in keywords:
        if keyw == 'ftag':
            ftag = keywords[keyw]
        if keyw == 'Silent':
            silent = keywords[keyw]
    
    ChainLength = len(data['istep'])
    #fnlinslope0 = lambda p, t: p[1]*t + p[0]
    #fnlinslope0 = lambda p, t: p[0]*np.exp(p[1]*t)
    #errfunc = lambda par, xdata, ydata: (fnlinslope0(par,xdata)-ydata)**2

    chain_stats = {}
    OutFileObject = open(OutStatFile,'w')
    
    for key in data.keys():
        # empty list for autocorrelation data
        x = []
        # skip the non-parameter data
        if isNonParam(key):
            pass
        else:
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
            while cval > lowtol or j < jmax:
                irange = np.arange(len(x1)-j)
                jrange = irange + j
                x1i_x1ipj = x1[irange]*x1[jrange]
                x1i_sq = (x1[irange]*x1[irange])
                x1i = (x1[irange])
                val = (np.mean(x1i_x1ipj) - (np.mean(x1i))**2)/\
                (np.mean(x1i_sq) - (np.mean(x1i))**2)
                cj.append(val)
                jarr.append(j)
                cval = val
                j += 1
            cj = np.array(cj)
            jarr = np.array(jarr)
            corlen_index = np.where( np.abs(cj-0.5e0) == np.min( np.abs(cj-0.5e0)) )[0]
            #print corlen_index
            corlen = jarr[corlen_index[0]]
            efflen = long(float(ChainLength)/float(corlen))
            if mkPlotsFlag:
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

def isNonParam(key):
    """
        checks if a given MCMC data key is not a model parameter.
    """
    
    if key == 'acr' or key == 'frac' or key == 'chi1'\
    or key == 'chi2' or key == 'istep':
        return True
    else:
        return False