
import os
import sys
import cPickle as pickle
import tmcmc
from tmcmc import DataFuncPrep as dfp
from tmcmc import class_fitprep as cfp
import pylab as plt
import numpy as np

Object = cfp.Object(sys.argv[1])

DataPrepPath = cfp.DataPrepPath
FracRej = {}

for fileName in os.listdir(cfp.PicklePath):
    if fileName.startswith(Object.name+'.FracRej'):
        FilePath = cfp.PicklePath+fileName
        #prinst FilePath
        if not fileName.endswith('pickle'):
            FileObj = open(FilePath,'r')
            FileObj = FileObj.readlines()
            
            name_split = map(str, fileName.split('.'))
            AP = name_split[2]
            FracRej[AP] = {}
            for line in FileObj:
                #print line
                dsplit = map(str, line.split('|'))
                if len(dsplit) > 1:
                    AP = dsplit[0].strip()
                    TT = dsplit[1].strip()
                    fRej = float(dsplit[2])
                    FracRej[AP][TT] = fRej

OptAp = pickle.load(open(cfp.PicklePath+Object.name+'.OptAp.pickle','rb'))
FluxNorm = pickle.load(open(cfp.PicklePath+Object.name+'.FluxNorm.pickle','rb'))
#FracRej = pickle.load(open(cfp.PicklePath+Object.name+'.FracRej.pickle','rb'))
PhotInfo = pickle.load(open(cfp.PicklePath+Object.name+'.PhotInfo.pickle','rb'))

PostDataPrepFile = Object.name+'.postDataPrep.table'

OutFile = open(PostDataPrepFile,'w')
print >> OutFile, '# Object = (%s) TT | OptAp |  RMS  | %Rej | Flux Normalization | err_scaling | med_err '

for TT in OptAp.keys():
    AP = str(int(OptAp[TT]['ap']))
    RMS = format(OptAp[TT]['min_rms']*1e6,'.0f')
    Rej = format(FracRej[AP][TT]*100,'.0f')+'%'
    sc = format(PhotInfo[TT]['err_scale'],'.6f')
    med_err = format(PhotInfo[TT]['med_err']*1e6,'.0f')
    #print FluxNorm[AP].keys()
    FNorm = str(FluxNorm[AP][TT])
    line = TT+' | '+AP+' | '+RMS+' | '+Rej+' | '+FNorm+' | '+sc+' | '+med_err
    print line
    print >> OutFile, line

fileOut = open(cfp.PicklePath+Object.name+'.FracRej.pickle','wb')
pickle.dump(FracRej,fileOut,-1)
fileOut.close()