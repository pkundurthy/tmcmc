#!/astro/apps/pkg/python64/bin//python

import tmcmc
import class_fitprep as cfp
import os, sys

def post_explore(ObjectName,Case,fitNum):
    
    Object = cfp.Object(ObjectName)
    Object.InitiateCase(Case)
    Object.InitiateFitNum(fitNum)

    Path = Object.casePath
    FileList = []
    
    for fileName in os.listdir(Path):
        if fileName.endswith('.expmcmc'):
            FileList.append(Path+fileName)
    
    Object.StepSizeFromExplore(FileList,0.02)
    Object.MakeStartFile(0e0)

if __name__ == '__main__':
    
    ObjectName = sys.argv[1]
    Case = sys.argv[2]
    fitNum = sys.argv[3]
    post_explore(ObjectName,Case,fitNum)
