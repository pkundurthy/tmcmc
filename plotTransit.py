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
    
    
def OtherFitLabels(CaseName):
    """             """
    
    colorList = ['c','m','r']
    symList = ['*','h','H','D','^','v']

def FitLabels(CaseName):
    """             """

    fitLabel = None
    mtype = None
    mcolor = None
    Other_WASP2_Fits = {}
    Other_GJ1214_Fits = {'charbonneau2009':(r'Charbonneau et al. (2009)','s','b'),\
                         'sada2010':(r'Sada et al. (2010)','*','b'),\
                         'carter2011':(r'Carter et al. (2011)','^','b'),\
                         'kundurthy2011':(r'Kundurthy et al. (2011)','o','b'),\
                         'berta2011':(r'Berta et al. (2011)','H','b'),\
                         'bean2011':(r'Bean et al. (2011)','D','b'),\
                         'croll2011':(r'Croll et al. (2011)','<','b'),\
                         'desert2011':(r'D{\'e}sert et al. (2011)','>','b'),\
                         'demooij2012':(r'de Mooij et al. (2012)','v','b'),\
                         'berta2012':(r'Berta et al. (2012)','h','b') }

    Other_XO2_Fits = {'burke2007':(r'Burke et al. (2007)','*','b'),\
                      'fernandez2009':(r'Fernandez et al. (2009)','D','b'),\
                      'sing2011':(r'Sing et al. (2011)','s','b')}

    Other_TRES3_Fits = {'odonovan2007':(r'O\'Donovan et al. (2007)','^','b'),\
                 'sozzetti2009':(r'Sozetti et al. (2009)','s','b'),\
                 'gibson2009':(r'Gibson et al. (2009)','D','b'),\
                 'christiansen2011':(r'Christiansen et al. (2011)','*','b'),\
                 'lee2011':(r'Lee et al. (2011)','v','b'),\
                 'sada2012':(r'Sada et al. (2012)','s','b'),\
                 'southworth2011':(r'Southworth (20011)','H','b')}
    OtherFits = {}
    OtherFits.update(Other_GJ1214_Fits)
    OtherFits.update(Other_XO2_Fits)
    OtherFits.update(Other_TRES3_Fits)

    if CaseName.lower().startswith('mcmc'):
        fitLabel = r'APOSTLE (TMCMC)'
        mtype = 'o'
        mcolor = 'k'
    elif CaseName.lower().startswith('minuit'):
        fitLabel = r'APOSTLE (Minuit)'
        mtype = 's'
        mcolor = 'b'
    elif CaseName.lower().startswith('tap'):
        fitLabel = r'APOSTLE (TAP)'
        mtype = 'o'
        mcolor = 'w'
    else:
        fitLabel,mtype,mcolor = OtherFits[CaseName]

    return fitLabel,mtype,mcolor

def returnTsub(TSTAMP):
    """ For a parameter with transit time tag, 
    return latex symbol
    """

    if TSTAMP.startswith('T'):
        Tsplit = map(str, TSTAMP.split('.'))
        if len(Tsplit) == 1:
            Tnum = long(Tsplit[0].strip('T'))
        else:
            Tnum = long(Tsplit[1].strip('T'))

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

def TableEntry(errEntry,par,fStr):

    Entry = 'Wrong'

    if par == 'Period':
        Val = format(errEntry[par]['value'],fStr)
    elif par.startswith('T0'):
        Val = format(errEntry[par]['value'],fStr)
    else:
        Val = format(errEntry[par]['value'],fStr)

    if np.isnan(errEntry[par]['lower']) or \
       np.isnan(errEntry[par]['upper']):
        Entry = '('+format(errEntry[par]['value'],fStr)+')'
    elif (errEntry[par]['lower'] != errEntry[par]['upper']) and \
        not errEntry[par]['useSingle']:
        Upp = format(errEntry[par]['upper'],fStr)
        Low = format(errEntry[par]['lower'],fStr)
        if float(Upp) == 0e0 or float(Low) == 0e0:
            maxerr = max([errEntry[par]['upper'],errEntry[par]['lower']])
            errPart = '$\pm$'+format(maxerr,fStr) 
            Entry = Val+errPart
        elif float(Upp) == float(Low):
            maxerr = max([errEntry[par]['upper'],errEntry[par]['lower']])
            errPart = '$\pm$'+format(maxerr,fStr) 
            Entry = Val+errPart
        else:
            errPart = '$^{+'+Upp+'}_{-'+Low+'}$'
            Entry = Val+errPart
    else:
        maxerr = max([errEntry[par]['upper'],errEntry[par]['lower']])
        errPart = '$\pm$'+format(maxerr,fStr)
        Entry = Val+errPart

    return Entry

def TUString(parName):

    if parName.startswith('T0'):
        UString = 'BJD'
    elif parName.startswith('vel'):
        UString = 'days$^{-1}$'
    elif parName == 'tT':
        UString = 'days'
    elif parName == 'tG':
        UString = 'days'
    elif parName == 'Period':
        UString = r'Period+ (sec)'
    elif parName == 'inc':
        UString = r'$^{o} (deg)$'
    elif parName.startswith('rho'):
        UString = 'g/cc'
    else:
        UString = '-'
        
    return UString

def TForm(parName,**kwargs):

    if parName.startswith('T0'):
        parSym = '$T_{mid}$ - '+returnTsub(parName)
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
        parSym = r'$(R_{p}/R_{\star})_{\textrm{(%s)}}$' % (TT)
        AxFormat = FormatStrFormatter('%.4f')
    elif parName.startswith('vel'):
        parSym = r'$\nu/R_{\star}$'
        AxFormat = FormatStrFormatter('%.2f')
    elif parName == 'tT':
        parSym = r'$t_{T}$'
        AxFormat = FormatStrFormatter('%.4f')
    elif parName == 'tG':
        parSym = r'$t_{G}$'
        AxFormat = FormatStrFormatter('%.4f')
    elif parName.startswith('aRs'):
        parSym = r'$a/R_{\star}$'
        AxFormat = FormatStrFormatter('%.2f')
    elif parName == 'b':
        parSym = r'b'
        AxFormat = FormatStrFormatter('%.2f')
    elif parName == 'Period':
        parSym = r'Period+ (sec)'
        AxFormat = FormatStrFormatter('%.2f')
    elif parName == 'inc':
        parSym = r'$i_{orb}$'
        AxFormat = FormatStrFormatter('%.2f')
    elif parName.startswith('rho'):
        parSym = r'$\rho_{\star}$'
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
    
    MD = False
    objectName = ''
    
    for key in kwargs:
        if key.lower().startswith('multidepth'):
            MD = kwargs[key]
        if key.lower().startswith('object'):
            objectName = kwargs[key]
            
    if parName.startswith('T0'):
        parSym = returnTsub(parName)
    elif parName.startswith('D'):
        msplit = map(str,parName.split('.'))
        if not MD:
            TT = returnTsub(msplit[1]).strip('$')+' '
            TT = Tfilter(TT,objectName)
            #TT = Tfilter(TT,objectName)
            parSym = '$'+msplit[0]+'_{(%s)}$' % TT
        else:
            TT = msplit[1].strip('T')
            parSym = '$'+msplit[0]+'_{(%s)}$' % TT
        #print parSym
    elif parName == 'tT':
        parSym = r'$t_{T}$'
    elif parName == 'tG':
        parSym = r'$t_{G}$'
    elif parName.startswith('v1.') or parName.startswith('v2.'):
        msplit = map(str,parName.split('.'))
        TT = ''
        for i in range(len(msplit)):
            if i > 0: TT += returnTsub(msplit[i]).strip('$')+' '
        for key in kwargs:
            if key.lower().startswith('object'):
                objectName = kwargs[key]
                TT = Tfilter(TT,objectName)
            else:
                pass
        parSym = '$'+msplit[0]+'_{(%s)}$' % TT
    elif parName.startswith('vel'):
        parSym = r'$\nu/R_{\star}$'
    else:
        parSym = parName

    return {'label':parSym}

def TransitParFormat(parlist,**kwargs):
    """                     """

    parFormDict = {}
    for par in parlist:
        parFormDict[par] = TForm(par,**kwargs)

    return parFormDict

def TransitStatParFormat(parlist,**kwargs):
    """                     """

    parFormDict = {}
    for par in parlist:
        parFormDict[par] = TStatForm(par,**kwargs)

    return parFormDict

def TData(d,parName,par1):

    if parName.startswith('T0'):
        x = ((np.array(d) - par1)*86400e0).tolist()
        d = x
    elif parName.startswith('Period'):
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

def PrepTransitData(MCMCFileList,parlist,BestFitPar):

    parData = {}
    axisData = {}
    
    if type(MCMCFileList) is list:
        DataFile = MCMCFileList
    else:
        DataFile = [MCMCFileList]

    for par in parlist:
        try:
            x = read1parMCMC(DataFile[0],par)
        except:
            x = read1parMCMC(DataFile[1],par)
        d = x[par]
        parData[par] = TData(d,par,BestFitPar[par]['value'])
        rg0,rg1 = getRange(parData[par])
        axisData[par] = {'axisRange':(rg0,rg1),'axisTicks':axisTicks(rg0,rg1)}

    return parData, axisData

def parErr4Plot(parErr):
    """ convert error dict to one useable by plotmcmc """

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
    """  return 1-sigma    """

    x = x-np.median(x)
    dsort = np.sort(x)
    npts = len(x)
    sigma = (x[.8415*npts]-x[.1585*npts])/2e0

    return sigma

def parPeriodDay2Sec(pars,bestFitPars):
    """ change period days to seconds """
    
    for par in pars.keys():
        if par.startswith('Period'):
            pars[par]['value'] = (pars[par]['value'] -\
            bestFitPars[par]['value'])*86400e0
            pars[par]['step'] =[pars[par]['step'][0]*86400e0,\
                                pars[par]['step'][1]*86400e0]
    
    return pars

def parTimeDay2Sec(pars,bestFitPars):
    """ change times in parameters from days to seconds """

    for par in pars.keys():
        if par.startswith('T0'):
            pars[par]['value'] = (pars[par]['value'] -\
            bestFitPars[par]['value'])*86400e0
            pars[par]['step'] =[pars[par]['step'][0]*86400e0,\
                                pars[par]['step'][1]*86400e0]

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
        