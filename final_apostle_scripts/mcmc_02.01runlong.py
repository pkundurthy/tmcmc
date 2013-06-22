#!/astro/apps/pkg/python64/bin//python

import tmcmc
from tmcmc import class_fitprep as cfp
import sys

def run_mcmc(ObjectName,Case,fitNum,nsteps):
    
    Object = cfp.Object(ObjectName)
    Object.InitiateCase(Case)
    Object.InitiateFitNum(fitNum)
    Object.InitiateData()


    x = cfp.chainPrep(Object)

    OutFile = Object.OutFitFile

    tmcmc.mcmc.mcmc_mh_adapt(nsteps,Object.FuncName,\
                             Object.ObservedData,\
                             x.ModelParams,\
                             x.NuisanceData,\
                             Object.BoundParams,\
                             False,False,\
                             OutFile,True)

if __name__ == '__main__':
    
    ObjectName = sys.argv[1]
    Case = sys.argv[2]
    fitNum = sys.argv[3]
    nsteps = float(sys.argv[4])
    
    run_mcmc(ObjectName,Case,fitNum,nsteps)