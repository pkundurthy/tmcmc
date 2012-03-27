import itertools
from iopostmcmc import read1parMCMC
from matplotlib.ticker import FormatStrFormatter
from matplotlib.font_manager import fontManager, FontProperties
from plotmcmc import getRange, axisTicks
from tmcmc.iomcmc import ReadStartParams
import numpy as np
import sys
from matplotlib import rc
rc('text',usetex=True)
rc('font',family='serif')

if sys.version_info[1] < 6:
    from tmcmc.misc import format

def returnTsub(TSTAMP,**kwargs):
    """ For a parameter with transit time tag, 
    return latex symbol
    """

    if TSTAMP.startswith('T'):
        Tsplit = map(str, TSTAMP.split('.'))
        if len(Tsplit) == 1:
            Tnum = long(Tsplit[0].strip('T'))
        else:
            Tnum = long(Tsplit[1].strip('T'))
        for key in kwargs:
            if key.lower().startswith('object'):
                objectname = kwargs[key]
                if objectname.lower() == 'xo2':
                    Tnum = str(int(Tnum)-1)
                else:
                    pass
        Tsub = '$T_{%s}$' % Tnum
    else:
        Tsub = 'Wrong'

    return Tsub

def Tfilter(TT,objectName):

    if objectName.lower() == 'xo2':
        if TT.startswith('T_{1}'):
            TT = 'I'
        elif TT.startswith('T_{7}'):
            TT = 'r\''
    elif objectName.lower() == 'wasp2':
        if TT.startswith('T_{1}'):
            TT = 'I'
        elif TT.startswith('T_{8}'):
            TT = 'r\''
    elif objectName.lower() == 'tres3':
        TT = 'r\''
    elif objectName.lower() == 'gj1214':
        TT = 'r\''

    return TT

def TForm(parName,**kwargs):
    
    if parName.startswith('T0'):
        parSym = '$T_{mid}$ - '+returnTsub(parName,**kwargs)
        AxFormat = FormatStrFormatter('%.3f')
    elif parName.startswith('D'):
        msplit = map(str,parName.split('.'))
        TT = ''
        Sym = ''
        for i in range(len(msplit)):
            if i > 0:
                TT += returnTsub(msplit[i]).strip('$')+' '
        for key in kwargs:
            if key.lower().startswith('object'):
                objectName = kwargs[key]
                TT = Tfilter(TT,objectName)
                Sym = r'$D_{\textrm{(%s)}}$' % (TT)
            else:
                TT = TT.strip('T_{')
                TT = TT[:-2]
                Sym = r'$D_{\textrm{%s}}$' % (TT)
        parSym = Sym
        AxFormat = FormatStrFormatter('%.4f')
    elif parName.startswith('u1.') or parName.startswith('u2.'):
        msplit = map(str,parName.split('.'))
        TT = ''
        for i in range(len(msplit)):
            if i > 0:
                TT += returnTsub(msplit[i]).strip('$')+' '
        for key in kwargs:
            if key.lower().startswith('object'):
                objectName = kwargs[key]
                TT = Tfilter(TT,objectName)
            else:
                pass
        symb = msplit[0][0]
        subs = msplit[0][1]
        parSym = r'$%s_%s{\textrm{(%s)}}$' % (symb,subs,TT)
        AxFormat = FormatStrFormatter('%.4f')
    elif parName.startswith('v1.') or parName.startswith('v2.'):
        msplit = map(str,parName.split('.'))
        TT = ''
        for i in range(len(msplit)):
            if i > 0:
                TT += returnTsub(msplit[i]).strip('$')+' '
        for key in kwargs:
            if key.lower().startswith('object'):
                objectName = kwargs[key]
                TT = Tfilter(TT,objectName)
            else:
                pass
        symb = msplit[0][0]
        subs = msplit[0][1]
        parSym = r'$%s_%s{\textrm{(%s)}}$' % (symb,subs,TT)
        AxFormat = FormatStrFormatter('%.4f')
    elif parName.startswith('RpRs'):
        msplit = map(str,parName.split('.'))
        TT = ''
        for i in range(len(msplit)):
            if i > 0: 
                TT += returnTsub(msplit[i]).strip('$')+' '

        for key in kwargs:
            if key.lower().startswith('object'):
                objectName = kwargs[key]
                TT = Tfilter(TT,objectName)
            else:
                pass
        parSym = r'$(R_{p}/R_{*})_{\textrm{(%s)}}$' % (TT)
        AxFormat = FormatStrFormatter('%.4f')
    elif parName.startswith('vel'):
        parSym = r'$\nu/R_{*}$'
        AxFormat = FormatStrFormatter('%.2f')
    elif parName == 'tT':
        parSym = r'$\tau_{T}$'
        AxFormat = FormatStrFormatter('%.4f')
    elif parName == 'tG':
        parSym = r'$\tau_{G}$'
        AxFormat = FormatStrFormatter('%.4f')
    elif parName.startswith('aRs'):
        parSym = r'$a/R_{*}$'
        AxFormat = FormatStrFormatter('%.4f')
    elif parName.startswith('rho'):
        parSym = r'$\rho_{*}$'
        AxFormat = FormatStrFormatter('%.2f')
    elif parName.startswith('sigwhite'):
        parSplit = map(str,parName.split('.'))
        Num = parSplit[1].strip('T')
        parSym = '$\sigma_{w,T%s}$' % Num
        AxFormat = FormatStrFormatter('%.4f')
    elif parName.startswith('sigred'):
        parSplit = map(str,parName.split('.'))
        Num = parSplit[1].strip('T')
        parSym = '$\sigma_{r,%s}$' % Num
        AxFormat = FormatStrFormatter('%.4f')
    else:
        parSym = parName
        AxFormat = None
        
    return {'label':parSym,'axForm':AxFormat}
    
def TransitTableFormat(allpars,**kwargs):
    """
    """
    
    parFormDict = {}
    for par in parlist:
        parFormDict[par] = TForm(par,**kwargs)

    return parFormDict

def TStatForm(parName,**kwargs):
    
    if parName.startswith('T0'):
        parSym = returnTsub(parName,**kwargs)
    elif parName.startswith('D'):
        msplit = map(str,parName.split('.'))
        TT = ''
        for i in range(len(msplit)):
            if i > 0: 
                TT += returnTsub(msplit[i],**kwargs).strip('$')+' '
        for key in kwargs:
            if key.lower().startswith('object'):
                objectName = kwargs[key]
                TT = Tfilter(TT,objectName)
            else:
                pass
        parSym = '$'+msplit[0]+'_{(%s)}$' % TT
    elif parName == 'tT':
        parSym = r'$\tau_{T}$'
    elif parName == 'tG':
        parSym = r'$\tau_{G}$'
    elif parName.startswith('v1.') or parName.startswith('v2.'):
        msplit = map(str,parName.split('.'))
        TT = ''
        for i in range(len(msplit)):
            if i > 0: TT += returnTsub(msplit[i],**kwargs).strip('$')+' '
        for key in kwargs:
            if key.lower().startswith('object'):
                objectName = kwargs[key]
                TT = Tfilter(TT,objectName)
            else:
                pass
        parSym = '$'+msplit[0]+'_{(%s)}$' % TT
    elif parName.startswith('vel'):
        parSym = r'$\nu/R_{*}$'
    else:
        parSym = parName

    return {'label':parSym}

def TransitParFormat(parlist,**kwargs):
    """
    """

    parFormDict = {}
    for par in parlist:
        parFormDict[par] = TForm(par,**kwargs)

    return parFormDict

def TransitStatParFormat(parlist,**kwargs):
    """
    """

    parFormDict = {}
    for par in parlist:
        parFormDict[par] = TStatForm(par,**kwargs)

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
    elif parName.startswith('v1.') or parName.startswith('v2.'):
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
    """ change times in parameters from days to seconds """
    
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

def ShortenTT(parLabels):
    
    for par in parLabels.keys():
        if '$T_{mid}$ - ' in parLabels[par]['label']:
             parLabels[par]['label'] = '$T_{%s}$' % parLabels[par]['label'].strip('$T_{mid} - ')
             
    return parLabels
        
def getxyparsFromParList(parList):
    """                 """
    
    xp = parList[:-1]
    yp = parList[::-1][:-1]
    
    return xp, yp

def makeStatLabels(Stats,DataFile):
    """     """
    
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

def getParFormat(name):
    """ assign parameter string format """
    
    if name == 'tT' or name == 'tG' or \
        name.startswith('v1.') or name.startswith('v2.') or \
        name.startswith('u1.') or name.startswith('u2.') or \
        name.startswith('RpRs.'):
        parformat = '.4f'

    if name.startswith('T0'):
        parformat = '.6f'
            
    if name.startswith('D.'):
        parformat = '.5f'

    if name == 'inc' or name == 'b' or\
       name == 'Period' or name == 'velRs' or\
       name == 'aRs' or name == 'rho_star':
        parformat = '.2f'

    return parformat
    
def getEntryString(value,lower,upper,useSingle,parformat):
    """                     """
    
    if useSingle:
        errVal = np.max([lower,upper])
        errStr = format(errVal,parformat)
        ValStr = format(value,parformat)
        EntryStr = r'%s $\pm$ %s' % (ValStr,errStr)
    else:
        if lower == upper:
            errVal = np.max([lower,upper])
            errStr = format(errVal,parformat)
            ValStr = format(value,parformat)
            EntryStr = r'%s $\pm$ %s' % (ValStr,errStr)
        else:
            errUpStr = format(upper,parformat)
            errLowStr = format(lower,parformat)
            ValStr = format(value,parformat)
            EntryStr = r'%s$^{+%s}_{-%s}$' % (ValStr,errUpStr,errLowStr)

    return EntryStr

def getUnitString(name):
    """              """
    
    NoUnits = '-'
    if name == 'tT' or name == 'tG' or \
        name.startswith('T0.'):
        UnitString = 'days'
    
    if name.startswith('v1.') or name.startswith('v2.') or \
        name.startswith('u1.') or name.startswith('u2.') or \
        name.startswith('RpRs.') or name.startswith('D.') or \
        name == 'b' or name == 'velRs' or name == 'aRs':
        UnitString = NoUnits

    if name == 'inc':
        UnitString = 'deg'
        
    if name == 'Period':
        UnitString = 'sec'
        
    if name == 'rho_star':
        UnitString = 'g/cc'
        
    return UnitString

class Parameter:
    
    def __init__(self, parName, value, upper, lower, useSingle, Object):

        self.name = parName
        self.value = value 
        self.upper = upper
        self.lower = lower
        self.useSingle = useSingle

        self.parformat = getParFormat(self.name)

        self.EntryString = getEntryString(self.value,self.lower,self.lower,self.useSingle,self.parformat)
        self.UnitString = getUnitString(self.name)

        parLabelFormat = TransitParFormat([parName],objectname=Object.name)
        parLabelFormat = ShortenTT(parLabelFormat)
        self.axForm = parLabelFormat[self.name]['axForm']
        self.LabelString = parLabelFormat[self.name]['label']