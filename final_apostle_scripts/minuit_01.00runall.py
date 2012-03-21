#!/astro/apps/pkg/python64/bin//python

import tmcmc
import class_fitprep as cfp
import sys

def run_minuit(ObjectName,Case,fitNum):
    
    Object = cfp.Object(ObjectName)
    Object.InitiateCase(Case)
    if Object.fitMethod.lower() != 'minuit':
        raise NameError("Fit method initiated %s is not Minuit" % Object.fitMethod)
    
    Object.InitiateFitNum(fitNum)

    x = cfp.chainPrep(Object)

    tmcmc.runminuit.RunMinuit(Object.FuncName,x.ObservedData,\
            x.ModelParams,x.NuisanceData,x.BoundParams,1e0,Object.OutFitFile)

if __name__ == '__main__':
    
    for ObjectName in ['TRES3','XO2','WASP2']:
        for Case in ['MINUIT.FLD','MINUIT.OLD','MINUIT.MDFLD']:
            for fitNum in [1,2]:
                print 'Running, '+ObjectName+' '+Case+' '+str(fitNum)
                run_minuit(ObjectName,Case,fitNum)
