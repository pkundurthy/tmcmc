#!/astro/apps/pkg/python64/bin//python

import tmcmc
from tmcmc import class_fitprep as cfp
import sys

def post_minuit(ObjectName,Case,fitNum):
    """             """
    
    Object = cfp.Object(ObjectName)
    Object.InitiateCase(Case)
    Object.InitiateFitNum(fitNum)

    tmcmc.derived_MTQ_2011.printDerivedParFile_MTQ_2011(Object.OutFitFile,Object.DerivedParFile)
    
    tmcmc.runminuit.MinuitPar2Err(Object.OutParFile,Object.ParErrorFile)
    tmcmc.runminuit.MinuitPar2Err(Object.DerivedParFile,Object.DerivedErrorFile)
    tmcmc.runminuit.MergeErrFiles(Object.ParErrorFile,Object.DerivedErrorFile)

if __name__ == '__main__':
    
    ObjectName = sys.argv[1]
    Case = sys.argv[2]
    fitNum = sys.argv[3]
    post_minuit(ObjectName,Case,fitNum)