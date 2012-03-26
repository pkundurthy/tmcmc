#!/astro/apps/pkg/python64/bin//python

import tmcmc
from tmcmc import class_fitprep as cfp
import sys

def run_post_mcmc(ObjectName,Case,fitNum,Stage):
    
    Object = cfp.Object(ObjectName)
    Object.InitiateCase(Case)
    Object.InitiateFitNum(fitNum)
    Object.InitiateData()
    
    x = cfp.chainPrep(Object)
    

    # cropping
    if Stage == 0 or Stage == 1:
        print 'Cropping MCMC'
        tmcmc.iopostmcmc.cropMCMC(Object.OutFitFile,Object.CroppedFileName,0.05,1e5)

    # auto-correlation & statistics
    if Stage == 0 or Stage == 2:
        print 'Autocorrelation Stats'
        lowtol = 0.01
        jmax = 5000
        makePlotsFlag = True
        res = 1
        tmcmc.postmcmc.autocorMCMC(Object.CroppedFileName,lowtol,jmax,\
                                   Object.AutoCorStatsFile,makePlotsFlag,silent=False,\
                                   ftag=Object.AutoCorFigRoot,resolution=res,dynamic=True)
    # print trace figures
    if Stage == 0 or Stage == 3:
        print 'Trace Plots'
        tmcmc.postmcmc.plotChain(Object.CroppedFileName, ftag=Object.TracePlotRoot)

    #covariance statistics
    if Stage == 0 or Stage == 4:
        print 'Covariance Stats'
        tmcmc.postmcmc.covcorStats(Object.CroppedFileName,Object.CovCorStatsRoot)

    # get lowest chisq
    if Stage == 0 or Stage == 5:
        print 'Lowest Chisq and Errors'
        tmcmc.iomcmc.WriteLowestChisq(Object.CroppedFileName,Object.ModelParams,\
                                      Object.LowestChiSQFile,True)
        tmcmc.iopostmcmc.printErrors(Object.CroppedFileName,Object.LowestChiSQFile,\
                                     Object.ParErrorFile)

if __name__ == '__main__':
    
    ObjectName = sys.argv[1]
    Case = sys.argv[2]
    fitNum = sys.argv[3]
    Stage = long(sys.argv[4])

    run_post_mcmc(ObjectName,Case,fitNum,Stage)