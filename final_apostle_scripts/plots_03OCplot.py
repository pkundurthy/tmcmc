#!/astro/apps/pkg/python64/bin//python

import os
import tmcmc
from tmcmc import class_fitprep as cfp
import sys
import optparse
import pylab as plt
import numpy as num
from matplotlib import rc
import matplotlib
from matplotlib import legend
rc('font',**{'family':'serif','serif':['Times New Roman'],'style':'semibold'})
rc('text',usetex=True)
from matplotlib.ticker import FormatStrFormatter,MaxNLocator, FixedLocator

width, height = matplotlib.rcParams['figure.figsize']
#print width, height
ObjectList = cfp.ObjectList

def CasePlotInformation(ParDict):
    """                 """
    
    CasePlotDict = {}
    for fitName in ParDict.keys():
        CasePlotDict[fitName] = tmcmc.plotTransit.FitLabels(fitName)

    return CasePlotDict

def OCplot(ObjectName):
    """             """

    ParDict, ParFiles, Object = cfp.getParDict(ObjectName)
    PeriodDicts = cfp.GetPeriodFits(ParDict)
    TTDicts = cfp.GetTTFits(ParDict)
    #UseList = ['MCMC.FLD.1','fernandez2009','sing2011','burke2007']
    #UseList = ['MCMC.FLD.1','fernandez2009','sing2011']
    CasePlotDict = CasePlotInformation(ParDict)
    for fitName in ParDict.keys():
        for parName in ParDict[fitName].keys():
            if parName.startswith('T0'):
                if fitName == 'TAP': fitName, parName, TTDicts[fitName]
    
    #print TTDicts['TAP']
    #plt.plot(xrange(len(TTDicts['TAP'][0])),TTDicts['TAP'][0],'b.')
    #plt.show()
    #sys.exit()
    UseList = {'XO2':['MCMC.FLD.1','fernandez2009','sing2011'],\
               'TRES3':['MCMC.FLD.2']}#,'sozzetti2009','gibson2009','christiansen2011']}

    #PeriodGuess = PeriodDicts['MCMC.FLD.1'][0]
    #print PeriodDicts['TAP'], PeriodDicts['MCMC.FLD.1']
    #sys.exit()
    #print PeriodDicts['TAP'][0],PeriodDicts['MCMC.FLD.1'][0]
    epoch, tt, err = cfp.sortTTdata(TTDicts,['TAP'],PeriodDicts['MCMC.FLD.1'][0])
    epoch1, tt1, err1 = cfp.sortTTdata(TTDicts,['MCMC.FLD.1'],PeriodDicts['MCMC.FLD.1'][0])
    #epoch, tt, err = cfp.sortTTdata(TTDicts,UseList[Object.name],PeriodGuess)
    (P,errP), (T0,errT0) = tmcmc.misc.linefitquick_werr(epoch,tt,err)
    (P1,errP1), (T01,errT01) = tmcmc.misc.linefitquick_werr(epoch1,tt1,err1)
    print (P,errP), (T0,errT0)
    print (P1,errP1), (T01,errT01)
    
    #sys.exit()
    #srt_epoch = sorted(epoch)
    #sortedTT = sorted(TTDicts['TAP'][0])
    #for i in range(len(srt_epoch)):
        #print i, srt_epoch[i], T0 + P*srt_epoch[i], sortedTT[i], sortedTT[i]-(T0 + P*srt_epoch[i])
        #ttRe = (tt[i]-P*epoch[i]) + P1*(epoch1[i])
        #reCastTT = tt[i]
        #print tt1[i]-ttRe,epoch1[i], epoch[i]
        #print epoch[i], epoch1[i], tt[0]+epoch1[i]*P1, tt1[i], tt[i]

    #sys.exit()
    yLine = T0+epoch*P
    yLine1 = T01+epoch1*P1
    OC = (tt-yLine)*86400e0
    OCerr = err*86400e0
    OC1 = (tt1-yLine1)*86400e0
    OCerr1 = err1*86400e0
    
    epoch = num.array(epoch)
    epoch1 = num.array(epoch1)
    argsort_epoch = num.argsort(epoch)
    argsort_epoch1 = num.argsort(epoch1)
    
    OC = OC[argsort_epoch]
    OCerr = OCerr[argsort_epoch]
    yLine = yLine[argsort_epoch]
    
    OC1 = OC1[argsort_epoch]
    OCerr1 = OCerr1[argsort_epoch]
    yLine1 = yLine1[argsort_epoch1]
    
    epoch = epoch[argsort_epoch]
    epoch1 = epoch1[argsort_epoch1]

    #print epoch
    #print epoch1
    #sys.exit()

    for i in range(len(OC1)):
        ovl = tmcmc.misc.ovl_coefficient(OC1[i],OCerr1[i],OC[i],OCerr[i])
        print i+1, epoch[i], OC[i], OCerr[i], OC1[i], OCerr1[i], ovl 
    print 'TT   nsigAPOSTLE  nsigTAP'
    for i in range(len(OC)):
        nsig1 = format(abs(OC1[i]/OCerr1[i]),'.1f')
        nsig2 = format(abs(OC[i]/OCerr[i]),'.1f')
        print i+1,',', nsig1,',', nsig2 
    
    ChiSQ1 = tmcmc.mcmc.chisq(OC,OCerr,num.zeros(len(OC)))
    ChiSQ2 = tmcmc.mcmc.chisq(OC1,OCerr1,num.zeros(len(OC1)))
    NPars = 2e0
    print 'red Chisq TAP, ChiSQ, DOF', ChiSQ1/(len(OC)-NPars), ChiSQ1, len(OC)-NPars
    print 'red Chisq MCMC, ChiSQ, DOF', ChiSQ2/(len(OC1)-NPars), ChiSQ2, len(OC1)-NPars
    plt.plot(epoch1,OC,'ko')
    #plt.plot(epoch1,OC1,'ks')
    plt.errorbar(epoch1,OC,yerr=OCerr,fmt=None,ecolor='blue')
    #plt.errorbar(epoch1,OC1,yerr=OCerr1,fmt=None,ecolor='green')
    plt.plot(epoch1,num.zeros(len(epoch)),'r-')
    plt.title(Object.name)
    plt.xlabel('Epoch')
    plt.ylabel('O-C (seconds)')
    plt.xlim([-15,max(epoch1)+15])
    plt.show()

if __name__ == '__main__':

    ObjectName = sys.argv[1]
    OCplot(ObjectName)