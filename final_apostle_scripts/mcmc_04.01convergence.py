#!/astro/apps/pkg/python64/bin//python

import tmcmc
from tmcmc import class_fitprep as cfp
import sys
import os

def GRStat(ObjectName,Case,fitList,lastn):

    Object = cfp.Object(ObjectName)
    Object.InitiateCase(Case)
    
    SplitFit = map(str, fitList.split(','))
    FileList = []
    for el in SplitFit:
        fitNum = el.strip('\"')
        Object.InitiateFitNum(fitNum)
        FileList.append(Object.CroppedFileName)

    GRFile = Object.casePath+'GRStats.'+Case+'.data'
    tmcmc.postmcmc.GelmanRubinConvergence(FileList,Object.StartFile,GRFile,lastn=lastn)

if __name__ == '__main__':

    ObjectName = sys.argv[1]
    Case = sys.argv[2]
    fitList = sys.argv[3]
    lastn = long(float(sys.argv[4]))
    
    GRStat(ObjectName,Case,fitList,lastn)
