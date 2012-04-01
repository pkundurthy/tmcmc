#!/astro/apps/pkg/python64/bin//python

import os
import tmcmc
from tmcmc import class_fitprep as cfp
from tmcmc import DataFuncPrep as dfp
import sys
import numpy as np

def runFinalizationCheck(ObjectName,condition):
    """ Check to see if we have satisfied the 5 major finalization criteria """

    # Condition 1 -- check for Statistically significant effective length
    Output1 = ""
    if condition == 0 or condition == 1:
        Output1 = '#|1|->\n#(1) Effective length check\n'+\
                  '# Eff < 1000 (Not Robust), 1000 < Eff'+\
                  ' < 10000 (Weak Significance), Eff > 10000 (Robust)\n'+\
                  '#Object |  Case    |  fitNum  | Eff  | par  | Significance  \n'

        Object = cfp.Object(ObjectName)
        for Case in ['MCMC.FLD','MCMC.OLD','MCMC.MDFLD']:
            for fitNum in [1,2]:
                Object.InitiateCase(Case)
                Object.InitiateFitNum(fitNum)
                parName, EffLength = tmcmc.iopostmcmc.getEffAutoCorStatFile(Object.AutoCorStatsFile)
                if EffLength < 1000:
                    sig = 'Bad'
                if 1000 <= EffLength < 10000:
                    sig = 'Weak'
                if EffLength >= 10000:
                    sig = 'Good'
                Output1 += '%s | %s | %s | %s | %s | %s \n' % \
                           (ObjectName,Case,str(fitNum),str(EffLength),parName,sig)

        Output1 += '#<-|1|\n'
        print Output1
        
    # Condition 2 -- check for Statistically significant effective length
    Output2 = ""
    if condition == 0 or condition == 2:
        Output2 = '#|2|->\n#(2) GRStat check\n'
        Output2 += 'Case  |Convergence Status | max GRStat | abs(delta(GR-1)) | max(Par)  \n'
        Object = cfp.Object(ObjectName)
        for Case in ['MCMC.FLD','MCMC.OLD','MCMC.MDFLD']:
            Object.InitiateCase(Case)
            for fileName in os.listdir(Object.casePath):
                if fileName.startswith('GRStat'):
                    FileObject = open(Object.casePath+fileName,'r')
                    FileObject = FileObject.readlines()
                    MaxGRStat = 1e0
                    MaxPar = ''
                    for line in FileObject:
                        SplitLine = map(str,line.split('='))
                        if len(SplitLine) == 2:
                            GRStat = float(SplitLine[1])
                            if GRStat > MaxGRStat:
                                MaxGRStat = GRStat
                                MaxPar = SplitLine[0].strip()
                    DeltaGR = np.abs(MaxGRStat-1e0)
                    Converge = 'False'
                    if DeltaGR < 1e-2:
                        Converge = 'True'
            Output2 += Case+'|'+Converge+'|'+str(MaxGRStat)+'|'+str(DeltaGR)+'|'+MaxPar+'\n'
        Output2 += '#<-|2|\n'
    print Output2

    # Condition 3 -- check for good reduced chisq for the lightcurve models
    Output3 = ""
    if condition == 0 or condition == 3:
        Output3 = '#|3|->\n#(3) Reduced CHISQ check\n'+\
                  '#Object |  Case    |  Chisq  | DOF  | redChiSQ \n'
        Object = cfp.Object(ObjectName)
        for Case in ['MCMC.FLD','MCMC.OLD','MCMC.MDFLD','MINUIT.FLD']:
            for fitNum in [1,2]:
                Object.InitiateCase(Case)
                Object.InitiateFitNum(fitNum)
                Object.UpdateModelParams()
                Object.InitiateData()
                NData = len(Object.DetrendedData['all']['x'])
                NOpen =  dfp.NOpen(Object.ModelParams)
                DOF =  NData - NOpen
                yobs = Object.DetrendedData['all']['y']
                yerr = Object.DetrendedData['all']['yerr']
                ymod = Object.ModelData['all']['y']
                ChiSQ = tmcmc.mcmc.chisq(yobs,yerr,ymod)
                RedChisq = float(ChiSQ)/float(DOF)
                Output3 += '%s | %s %s | %s | %s | %s \n' % \
                           (ObjectName,Case,str(fitNum),format(ChiSQ,'.2f'),format(DOF,'.0f'),format(RedChisq,'.2'))

        Output3 += '#<-|3|\n'
        print Output3
    
    OutFile = open(ObjectName+'/FitsFinalization.'+ObjectName+'.txt','w')
    print >> OutFile, Output1
    print >> OutFile, Output2
    print >> OutFile, Output3
    OutFile.close()

if __name__ == '__main__':

    ObjectList = map(str, sys.argv[1].split(','))
    condition = long(sys.argv[2])

    for Object in ObjectList:
        ObjectName = Object.strip('\"')
        runFinalizationCheck(ObjectName,condition)
