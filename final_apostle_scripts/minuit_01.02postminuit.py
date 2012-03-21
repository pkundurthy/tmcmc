#!/astro/apps/pkg/python64/bin//python

import tmcmc
import class_fitprep as cfp
import sys

def post_minuit(ObjectName,Case,fitNum):
    """             """
    
    Object = cfp.Object(ObjectName)
    Object.InitiateCase(Case)
    Object.InitiateFitNum(fitNum)

    tmcmc.derived_MTQ_2011.printDerivedParFile_MTQ_2011(Object.OutFitFile,Object.DerivedFile)

if __name__ == '__main__':
    
    ObjectName = sys.argv[1]
    Case = sys.argv[2]
    fitNum = sys.argv[3]
    post_minuit(ObjectName,Case,fitNum)