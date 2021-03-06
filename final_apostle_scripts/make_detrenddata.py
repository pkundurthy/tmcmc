#!/astro/apps/pkg/python64/bin//python

import tmcmc
from tmcmc import class_fitprep as cfp
import sys

def make_detrendData(ObjectName,Case,fitNum):

    Object = cfp.Object(ObjectName)
    Object.InitiateCase(Case)
    Object.InitiateFitNum(fitNum)
    Object.UpdateModelParams()
    Object.InitiateData()

    Object.printDetrendedData()

if __name__ == '__main__':
    
    for ObjectName in ['WASP2']: #['XO2','TRES3']: #,'WASP2']:
        for Case in ['MCMC.FLD']: #['MINUIT.FLD']:
            for fitNum in [1]:
                print 'writing, '+ObjectName+' '+Case+' '+str(fitNum)
                make_detrendData(ObjectName,Case,fitNum)
    