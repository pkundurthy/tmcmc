#!/astro/apps/pkg/python64/bin//python

import tmcmc
from tmcmc import class_fitprep as cfp
import sys

def genEXPcfg(Object,Case,NSteps):
    
    Object = cfp.Object(ObjectName)
    Object.InitiateCase(Case)
    NSteps = str(NSteps)
    
    CFGFileName = cfp.MainPath+\
                  'EXPLORE.'+Object.name+'.'+\
                  Object.case+'.cfg'

    Ofile = open(CFGFileName,'w')
    print >> Ofile, "Universe = Vanilla\n"
    print >> Ofile, "Executable = "+cfp.MainPath+"mcmc_01.01runexplore.py"
    print >> Ofile, "Initialdir = "+Object.casePath
    
    print >> Ofile, "Log = "+Object.casePath+"/"+Object.case+".EXPLORE.out"
    print >> Ofile, "error = "+Object.casePath+"/"+Object.case+".EXPLORE.err"
    
    print >> Ofile, "getenv = True \n\n"
    #"Output = "+MainPath+ChainName+"/"+ChainName+"."+ParName+".stuff",\

    OpenPars = cfp.OpenParArray(Object.ModelParams)

    for ParName in OpenPars:
        ChainLinesPerChain = [ \
        "Arguments = "+Object.name+" "+Object.case+" "+\
        ParName+" "+NSteps, \
        "Queue"]
        for el in ChainLinesPerChain:
            print >> Ofile, el
        print >> Ofile, '\n'

    Ofile.close()

if __name__ == '__main__':
    
    ObjectName = sys.argv[1] 
    Case = sys.argv[2]
    nsteps = sys.argv[3]
    genEXPcfg(ObjectName,Case,nsteps)
    
