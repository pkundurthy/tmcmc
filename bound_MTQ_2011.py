import numpy as np
import tqessential as tqe
from MTQ_2011 import *
import sys
if sys.version_info[1] < 6:
    from tmcmc.misc import format

def bound_v1_2011(ModelParams):
    """ checks if 0 < v1 < 1 """

    bound = True
    for key in ModelParams.keys():
        if key.startswith('v1'):
            v1 = ModelParams[key]['value']
            if v1 < 0e0 or v1 > 1e0:
                bound = False

    return bound

def bound_v1plusv2_2011(ModelParams):
    """ checks if v1 + v2 > 0 """

    bound = True
    for key in ModelParams.keys():
        if key.startswith('v1'):
            Tnumtags = ''
            arr = map(str, key.split('.'))
            # find transit number tags, similar to getting the filter tag
            for i in range(len(arr)-1):
                Tnumtags = Tnumtags+'.'+arr[i+1]
            v1pv2 = ModelParams['v1'+Tnumtags]['value'] + ModelParams['v2'+Tnumtags]['value']
            if v1pv2 < 0e0:
                bound = False
    return bound

def bound_D_2011(ModelParams):
    """ checks if D > 0 """

    bound = True
    for key in ModelParams.keys():
        if key.startswith('D.'):
            if ModelParams[key]['value'] < 0:
                bound = False

    return bound

def bound_tT_2011(ModelParams):
    """ checks if tT > 0 """

    bound = True
    if ModelParams['tT']['value'] < 0:
        bound = False

    return bound

def bound_tG_2011(ModelParams):
    """ checks if tG > 0 """

    bound = True
    if ModelParams['tG']['value'] < 0:
        bound = False

    return bound
    
def bound_vfraction_MTQ_2011(ModelParams):
    """ checks if vel/Rstar > 0 """

    bound = True
    RefFilt = ModelParams['RefFilt']['printformat']
    Tags = tqe.getTags(ModelParams)
    tT = ModelParams['tT']['value']
    tG = ModelParams['tG']['value']
    
    checkD = bound_D_2011(ModelParams)
    if checkD:
        RpRs = []
        for par in ModelParams.keys():
            if par.startswith('D.'):
                parstrip = par.strip('D.')
                # gets D, v1, and v2 for a given filter
                D, v1, v2 = MTQ_FilterParams(parstrip,Tags,ModelParams)
                u1, u2 = tqe.LDC_v2u(v1,v2)
                RpRs.append((tqe.computeRpRs(u1,u2,tT,tG,D))**2)
            for el in RpRs:
                vfraction = el/(tT*tG)
                if vfraction < 0:
                    bound = False

    return bound
            
def bound_bfraction_MTQ_2011(ModelParams):
    """ checks if b > 0 """

    bound = True
    RefFilt = ModelParams['RefFilt']['printformat']
    Tags = tqe.getTags(ModelParams)
    tT = ModelParams['tT']['value']
    tG = ModelParams['tG']['value']
    
    checkD = bound_D_2011(ModelParams)
    if checkD:
        RpRs = []
        for par in ModelParams.keys():
            if par.startswith('D.'):
                parstrip = par.strip('D.')
                D, v1, v2 = MTQ_FilterParams(parstrip,Tags,ModelParams)
                u1, u2 = tqe.LDC_v2u(v1,v2)
                RpRs.append((tqe.computeRpRs(u1,u2,tT,tG,D)))
        for el in RpRs:
            bfraction = 1e0 - np.sqrt(el*(tT/tG))
            if bfraction < 0:
                bound = False

    return bound

def bound_bOVERaRs_MTQ_2011(ModelParams):
    """ checks if b/aRs <= 1 """
    
    tT = ModelParams['tT']['value']
    tG = ModelParams['tT']['value']
    Period = tqe.computePeriod(ModelParams)
    
    Tags = {}
    for pname in ModelParams.keys():
        if pname.startswith('v1'):
            StrArray = map(str,pname.split('.'))
            Tags[pname] = tqe.getFilterTags(StrArray)
        if pname.startswith('v2'):
            StrArray = map(str,pname.split('.'))
            Tags[pname] = tqe.getFilterTags(StrArray)
        if pname.startswith('D'):
            StrArray = map(str,pname.split('.'))
            Tags[pname] = tqe.getFilterTags(StrArray)
    
    RefFilt = ModelParams['RefFilt']['printformat']
    Dref, v1ref, v2ref = MTQ_FilterParams(RefFilt,Tags,ModelParams)
    u1ref = (v1ref+v2ref)/2e0
    u2ref = (v1ref-v2ref)/2e0
    TransitRef = MTQ_getDerivedParams(Dref,tT,tG,u1ref,u2ref,Period)
    
    bound = True
    if TransitRef['b']/TransitRef['aRs'] > 1e0:
        bound = False
        
    return bound