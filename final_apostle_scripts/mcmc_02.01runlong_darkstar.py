#!/usr/bin/python

import sys
import socket

if socket.gethostname().lower() == 'darkstar.astro.washington.edu':
    sys.path = ['','/astro/users/pkundurthy/ENV/pyminuit2/lib',\
                   '/astro/users/pkundurthy/ENV/python',\
                   '/astro/apps/pkg/python64/lib/python26.zip',\
                   '/astro/apps/pkg/python64/lib/python2.6',\
                   '/astro/apps/pkg/python64/lib/python2.6/plat-linux2',\
                   '/astro/apps/pkg/python64/lib/python2.6/lib-tk',\
                   '/astro/apps/pkg/python64/lib/python2.6/lib-old',\
                   '/astro/apps/pkg/python64/lib/python2.6/lib-dynload',\
                   '/astro/apps/pkg/python64/lib/python2.6/site-packages',\
                   '/astro/apps/pkg/python64/lib/python2.6/site-packages/PIL']
                   
import tmcmc
import class_fitprep as cfp

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