#!/astro/apps/pkg/python64/bin//python

import os
import tmcmc
from tmcmc import class_fitprep as cfp
import sys
import optparse
import pylab as plt
import numpy as num
import math
from matplotlib import rc
import matplotlib
from matplotlib import legend
rc('font',**{'family':'serif','serif':['Times New Roman'],'style':'semibold'})
rc('text',usetex=True)
from matplotlib.ticker import FormatStrFormatter,MaxNLocator, FixedLocator
import itertools

def DiffTable(ObjectName):
    """             """
    
    ParDict, ParFiles, Object = cfp.getParDict(ObjectName)

    #print ParDict['MINUIT.FLD.1']['NT.T4']['lower']
    #sys.exit()
    FitList = ParFiles.keys()
    allParList = []
    for fit in ParDict.keys(): allParList.extend(ParDict[fit].keys())
    CommonParList = list(set(allParList))
    CommonParList = ['T0.T1'] 
    
    TriedPairList = []
    for par in CommonParList:
        if par in Object.ModelParams.keys():
            pf = Object.ModelParams[par]['printformat']
        else:
            Object.InitiateCase('MCMC.FLD')
            Object.InitiateFitNum('1')
            Dpar = tmcmc.iomcmc.ReadStartParams(Object.DerivedLowestChiSQFile)
            pf = Dpar[par]['printformat']

        for pair in list(itertools.permutations(FitList,2)):
            if not pair in TriedPairList and \
               not pair[::-1] in TriedPairList and \
               not pair[0] in [pair[1]]:
                TriedPairList.append(pair)
                try:
                    #print ParDict[pair[0]][par].keys()
                    #print ParDict[pair[1]][par].keys()
                    #print pair, par
                    mu1 = ParDict[pair[0]][par]['value']
                    mu2 = ParDict[pair[1]][par]['value']
                    sig1 = max([ParDict[pair[0]][par]['lower'],ParDict[pair[0]][par]['upper']])
                    sig2 = max([ParDict[pair[1]][par]['lower'],ParDict[pair[1]][par]['upper']])
                    pstring_m1 = format(mu1,pf)
                    pstring_s1 = format(sig1,pf)
                    pstring_m2 = format(mu2,pf)
                    pstring_s2 = format(sig2,pf)
                    #print mu1, mu2, sig1, sig2, pair, par, ovl
                    if par == 'Period':
                        ovl = tmcmc.misc.ovl_coefficient(mu1*86400e0,sig1*86400e0,mu2*86400e0,sig2*86400e0)
                    else:
                        ovl = tmcmc.misc.ovl_coefficient(mu1,sig1,mu2,sig2) 
                    
                    #print mu1, mu2, sig1, sig2, pair, par, ovl
                    Nwidth = 13
                    if ovl > 1e-2:
                        #print par, pair[0], pair[1], ovl, (mu1,sig1),(mu2,sig2),' Good'
                        print par, pair[0].strip().ljust(Nwidth),(pstring_m1,pstring_s1),pair[1].strip().ljust(Nwidth),(pstring_m2,pstring_s2),'Good', ovl, num.abs(mu1-mu2)/max([sig1,sig2])
                    elif not math.isnan(ovl):
                        print par, pair[0].strip().ljust(Nwidth),(pstring_m1,pstring_s1),pair[1].strip().ljust(Nwidth),(pstring_m2,pstring_s2),'Bad ', ovl, num.abs(mu1-mu2)/max([sig1,sig2])
                    else:
                        #continue
                        print pair, ' Ugly'
                ##print mu1, sig1, mu2, sig2
                except:
                    #raise
                    pass

if __name__ == '__main__':

    ObjectName = sys.argv[1]
    #ParamName = sys.argv[2]

    DiffTable(ObjectName)