import tmcmc
from tmcmc import class_fitprep as cfp
import sys

RunFile = open('postExploreAll.csh','w')

iCount = 0
for ObjectName in ['TRES3','XO2','WASP2']:
    for Case in ['MCMC.FLD','MCMC.OLD','MCMC.MDFLD']:
        for fitNum in [1,2]:
            iCount += 1
            print './mcmc_01.02postexplore.py '+ObjectName+' '+Case+' '+str(fitNum)
            if iCount == 1:
                print >> RunFile, './mcmc_01.02postexplore.py '+ObjectName+' '+Case+' '+str(fitNum)+' > EXP.log'
                print >> RunFile, 'echo \"'+ObjectName+' '+Case+' '+str(fitNum)+'\"' 
            else:
                print >> RunFile, './mcmc_01.02postexplore.py '+ObjectName+' '+Case+' '+str(fitNum)+' >> EXP.log'
                print >> RunFile, 'echo \"'+ObjectName+' '+Case+' '+str(fitNum)+'\"'

print >> RunFile, 'grep \'NOT\' EXP.log'

RunFile.close()
