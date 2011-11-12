import itertools
from iopostmcmc import read1parMCMC
from matplotlib.ticker import FormatStrFormatter
from matplotlib.font_manager import fontManager, FontProperties
from plotmcmc import getRange, axisTicks
from tmcmc.iomcmc import ReadStartParams
import numpy as np
import sys
if sys.version_info[1] < 6:
    from tmcmc.misc import format


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
    
def TForm(parName):
    
    if parName.startswith('T0'):
        parSym = '$T_{mid}$ - '+returnTsub(parName)
        AxFormat = FormatStrFormatter('%.3f')
    elif parName.startswith('D'):
        msplit = map(str,parName.split('.'))
        TT = ''
        for i in range(len(msplit)): 
            if i > 0: 
                TT += returnTsub(msplit[i]).strip('$')+' '
        parSym = '$'+msplit[0]+'_{(%s)}$' % TT
        AxFormat = FormatStrFormatter('%.4f')
    elif parName == 'tT':
        parSym = r'$\tau_{T}$'
        AxFormat = FormatStrFormatter('%.4f')
    elif parName == 'tG':
        parSym = r'$\tau_{G}$'
        AxFormat = FormatStrFormatter('%.4f')
    elif parName.startswith('v'):
        msplit = map(str,parName.split('.'))
        TT = ''
        for i in range(len(msplit)):
            if i > 0: TT += returnTsub(msplit[i]).strip('$')+' '
        parSym = '$'+msplit[0]+'_{(%s)}$' % TT
        AxFormat = FormatStrFormatter('%.4f')
    else:
        parSym = parName
        AxFormat = None
        
    return {'label':parSym,'axForm':AxFormat}

def TransitParFormat(parlist):
    
    parFormDict = {}
    for par in parlist:
        parFormDict[par] = TForm(par)

    return parFormDict

def TData(d,parName,par1):
    
    if parName.startswith('T0'):
        x = ((np.array(d) - par1)*86400e0).tolist()
        d = x
    elif parName.startswith('D'):
        pass
    elif parName == 'tG':
        pass
    elif parName == 'tT':
        pass
    elif parName.startswith('v'):
        pass
    else:
        pass
        
    return d

def PrepTransitData(DataFile,parlist,BestFitPar):

    parData = {}
    axisData = {}
    for par in parlist:
        x = read1parMCMC(DataFile,par)
        d = x[par]
        parData[par] = TData(d,par,BestFitPar[par]['value'])
        rg0,rg1 = getRange(parData[par])
        axisData[par] = {'axisRange':(rg0,rg1),'axisTicks':axisTicks(rg0,rg1)}
        
    return parData, axisData

def parErr4Plot(parErr):
    """
    convert error dict to one useable by plotmcmc
    """
    
    outPar = {}
    for par in parErr.keys():
        if parErr[par]['useSingle']:
            err = max(parErr[par]['lower'],parErr[par]['upper'])
            parErr[par]['lower'] = err
            parErr[par]['upper'] = err
        outPar[par] = {'value':parErr[par]['value'],\
                       'step':[parErr[par]['lower'],\
                       parErr[par]['upper']]}
    return outPar

def robust1sigma(x):
    """
        return 1-sigma
    """
    x = x-np.median(x)
    dsort = np.sort(x)
    npts = len(x)
    sigma = (x[.8415*npts]-x[.1585*npts])/2e0
    
    return sigma

def parTimeDay2Sec(pars,bestFitPars):
    """
    change times in parameters from days to seconds
    """
    
    for par in pars.keys():
        if par.startswith('T0'):
            pars[par]['value'] = (pars[par]['value'] -\
            bestFitPars[par]['value'])*86400e0
            if isinstance(pars[par]['step'],list):
                for i in range(len(pars[par]['step'])):
                    pars[par]['step'][i] = pars[par]['step'][i]*86400e0
            else:
                pars[par]['step'] = (pars[par]['step'])*86400e0

    return pars

def makeStatLabels(Stats,DataFile):
    """
    
    """
    
    parList = getPars(DataFile)
    Npar = len(parList)
    iplot = 1
    
    StatLabels = {}

    for iy in range(Npar):
        for ix in range(Npar):
            if not ix >= iy:
                parName1 = parList[ix]
                parName2 = parList[iy]
                cov = r'$|\sigma_{(x,y)}|$='+\
                format(abs(Stats['cov'][parName1][parName2]['value']),'0.2f')
                spe = r'$|\rho|$='+\
                format(abs(Stats['spear'][parName1][parName2]['value']),'0.2f')
                pea = r'$|r|$='+\
                format(abs(Stats['pear'][parName1][parName2]['value']),'0.2f')
                StatLabels[iplot] = {'cov':cov,'spe':spe,'pea':pea}