import os
import tmcmc
import numpy as np
import itertools

LitFiles = {'fernandez09':{'par.der':'dataOther/fernandez09.par'},\
            'torres08':{'par.der':'dataOther/torres08.par'},\
            'sing11':{'par.der':'dataOther/sing11.par'} }
            


#def readTTV(filename):
    #"""
    #"""
    
    #dfile = open(filename,'r')
    #dfile = dfile.readlines()
    
    #TT = []
    #Epoch = []
    #err = []
    #ref = []
    #dsort = {}
    
    #for line in dfile:
        #if not line.startswith('#'):
            #dsplit = map(str, line.split('|'))
            #if dsplit[3].strip().strip('\n') != 'machalek09'\
               #and dsplit[3].strip().strip('\n') != 'burke07':
                #Epoch.append(float(dsplit[0]))
                #TT.append(float(dsplit[1]))
                #err.append(float(dsplit[2]))
                #ref.append(dsplit[3])
    
    #reflist = list(set(ref))
    #for cite in reflist:
        #dsort[cite.strip().strip('\n')] = {'x':[],'y':[],'yerr':[]}
    
    #for line in dfile:
        #if not line.startswith('#'):
            #dsplit = map(str, line.split('|'))
            #if dsplit[3].strip().strip('\n') != 'machalek09' \
               #and dsplit[3].strip().strip('\n') != 'burke07':
                #dsort[dsplit[3].strip()]['x'].append(float(dsplit[0]))
                #dsort[dsplit[3].strip()]['y'].append(float(dsplit[1]))
                #dsort[dsplit[3].strip()]['yerr'].append(float(dsplit[2]))
    
    #return Epoch,TT,err,ref, dsort

