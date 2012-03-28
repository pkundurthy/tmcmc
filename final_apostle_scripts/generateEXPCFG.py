#!/astro/apps/pkg/python64/bin//python

import tmcmc
import class_fitprep as cfp
import sys

def generateCFGEXP():
    
    nsteps = 4e4
    RunFile = open('allCFGEXP.csh','w')
    
    for ObjectName in ['TRES3','XO2','WASP2']:
        for Case in ['MCMC.FLD','MCMC.OLD','MCMC.MDFLD']: 
            Object = cfp.Object(ObjectName)
            Object.InitiateCase(Case)
            NSteps = str(nsteps)
    
            OpenPars = cfp.OpenParArray(Object.ModelParams)
        
            for ParName in OpenPars:
                print "./mcmc_01.01runexplore.py "+Object.name+" "+Object.case+" "+\
                    ParName+" "+NSteps
                print >> RunFile, "./mcmc_01.01runexplore.py "+Object.name+" "+Object.case+" "+\
                    ParName+" "+NSteps

    RunFile.close()

if __name__ == '__main__':
    
    generateCFGEXP()
