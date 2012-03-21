#!/astro/apps/pkg/python64/bin//python

import tmcmc
import class_fitprep as cfp
import sys

def run_explore(ObjectName,Case,param,nsteps):
    
    Object = cfp.Object(ObjectName)
    Object.InitiateCase(Case)
    if Object.fitMethod.lower() != 'mcmc':
        raise NameError("given fit method (%s) is not MCMC" % Object.fitMethod)

    x = cfp.chainPrep(Object)
    x.setForExplore(param)

    OutFile = Object.casePath+Object.name+'.'+Object.fitID+'.'+param+'.expmcmc'

    tmcmc.mcmc.mcmc_mh_adapt(nsteps,x.FuncName,\
                             x.ObservedData,\
                             x.ModelParams,\
                             x.NuisanceData,\
                             x.BoundParams,\
                             False,True,\
                             OutFile,True)

if __name__ == '__main__':
    
    ObjectName = sys.argv[1] 
    Case = sys.argv[2]
    param = sys.argv[3]
    nsteps = float(sys.argv[4])
    run_explore(ObjectName,Case,param,nsteps)
    