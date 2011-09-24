import numpy as num
import os

os.system('idl < runp_robust.pro')

file = open('data4mean.txt','r')
fileLines = file.readlines()
data = []
from tmcmc.binning import MedianMeanOutlierRejection as medrej

for line in fileLines:
    data.append(float(line))
data = num.array(data)

mm, sdv, ngood, gi, bi = medrej(data, 5.0, 'median')
print 'PYTHON> 5sig =',mm,sdv,ngood,len(bi) 
mm, sdv, ngood, gi, bi = medrej(data, 3.0, 'median')
print 'PYTHON> 3sig =',mm,sdv,ngood,len(bi) 
mm, sdv, ngood, gi, bi = medrej(data, 0.9, 'median')
print 'PYTHON> 0.9sig =',mm,sdv,ngood,len(bi)

