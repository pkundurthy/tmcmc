#!/astro/apps/pkg/python64/bin//python

import tmcmc
from tmcmc import class_fitprep as cfp
import sys
import os

def print_derived(Object,Case,fitNum,Stage):
    
    Object = cfp.Object(ObjectName)
    Object.InitiateCase(Case)
    Object.InitiateFitNum(fitNum)
    Object.InitiateData()

    # stage 1
    if Stage == 0 or Stage == 1:
        print 'printing Derived ensemble'
        tmcmc.myderivedfunc.printDerived_MTQ_2011(Object.StartFile,Object.CroppedFileName,Object.CroppedDerivedFile)
    
    #stage 2
    if Stage == 0 or Stage == 2:
        print 'derived covcor Stats '
        tmcmc.postmcmc.covcorStats(Object.CroppedDerivedFile,Object.DerivedCovCorStatsRoot,derived=True)
    
    #stage 3
    if Stage == 0 or Stage == 3:
        print 'print derived'
        tmcmc.derived_MTQ_2011.printDerivedParFile_MTQ_2011(Object.LowestChiSQFile,Object.DerivedLowestChiSQFile)
    
    #stage 4
    if Stage == 0 or Stage == 4:
        print 'print Errors'
        tmcmc.iopostmcmc.printErrors(Object.CroppedDerivedFile,Object.DerivedLowestChiSQFile,Object.DerivedErrorFile)
        
    if Stage == 0 or Stage == 5:
        print 'Merge files'
        tmcmc.runminuit.MergeErrFiles(Object.ParErrorFile,Object.DerivedErrorFile)

if __name__ == '__main__':
    
    ObjectName = sys.argv[1]
    Case = sys.argv[2]
    fitNum = sys.argv[3]
    Stage = long(sys.argv[4])
    
    print_derived(ObjectName,Case,fitNum,Stage)