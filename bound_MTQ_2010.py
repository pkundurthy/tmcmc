
""" Contains the functions that set the bounds for various parameters in the model function. The user must add bounding functions suited to for their needs to this file."""
import numpy as np
import tqessential as tqe
import sys
if sys.version_info[1] < 6:
    from tmcmc.misc import format

def bound_u1plusu2_2010(ModelParams):
    """ checks if  0 < u1 + u2 < 1 """

    bound = True
    for key in ModelParams.keys():
        if key.startswith('u1'):
            Tnumtags = ''
            arr = map(str, key.split('.'))
            for i in range(len(arr)-1):
                Tnumtags = Tnumtags+'.'+arr[i+1]
            u1pu2 = ModelParams['u1'+Tnumtags]['value'] + ModelParams['u2'+Tnumtags]['value']
            if u1pu2 < 0 or u1pu2 > 1:
                bound = False

    return bound

def bound_u1_2010(ModelParams):
    """ checks if  u1 > 0 """

    bound = True
    for key in ModelParams.keys():
        if key.startswith('u1'):
            u1 = ModelParams[key]['value']
            if u1 < 0:
                bound = False

    return bound

def bound_v1_2010(ModelParams):
    """ checks if 0 < v1 < 1 """

    bound = True
    for key in ModelParams.keys():
        if key.startswith('v1'):
            v1 = ModelParams[key]['value']
            #print v1, ' v1'
            if v1 < 0e0 or v1 > 1e0:
                bound = False

    return bound

def bound_v1plusv2_2010(ModelParams):
    """ checks if v1 + v2 > 0 """

    bound = True
    for key in ModelParams.keys():
        if key.startswith('v1'):
            Tnumtags = ''
            arr = map(str, key.split('.'))
            for i in range(len(arr)-1):
                Tnumtags = Tnumtags+'.'+arr[i+1]
            v1pv2 = ModelParams['v1'+Tnumtags]['value'] + ModelParams['v2'+Tnumtags]['value']
            #print v1pv2, ' v1pv2'
            if v1pv2 < 0e0:
                bound = False
    return bound

def bound_D_2010(ModelParams):
    """ checks if D > 0 """

    bound = True
    for key in ModelParams.keys():
        if key.startswith('D.'):
            if ModelParams[key]['value'] < 0:
                bound = False

    return bound

def bound_RpRsSQ_2010(ModelParams):
    """ checks if RpRsSQ > 0 """

    bound = True
    if ModelParams['RpRsSQ']['value'] < 0:
        bound = False

    return bound

def bound_tT_2010(ModelParams):
    """ checks if tT > 0 """

    bound = True
    if ModelParams['tT']['value'] < 0:
        bound = False

    return bound

def bound_tG_2010(ModelParams):
    """ checks if tG > 0 """

    bound = True
    if ModelParams['tG']['value'] < 0:
        bound = False

    return bound

def bound_bfraction_2010(ModelParams):
    """ checks if b > 0 """

    bound = True
    checkRpRs = bound_RpRsSQ_2010(ModelParams)
    if checkRpRs:
        bfraction = 1e0 - np.sqrt(ModelParams['RpRsSQ']['value'])*(ModelParams['tT']['value']/ModelParams['tG']['value'])
        if bfraction < 0:
            bound = False

    return bound

def bound_vfraction_2010(ModelParams):
    """ checks if vel/Rstar > 0 """

    bound = True
    checkRpRs = bound_RpRsSQ_2010(ModelParams)
    if checkRpRs:
        vfraction = ModelParams['RpRsSQ']['value']/(ModelParams['tT']['value']*ModelParams['tG']['value'])
        if vfraction < 0:
            bound = False

    return bound

def bound_vfraction_withD_2010(ModelParams):
    """ checks if vel/Rstar > 0 """

    bound = True
    checkD = bound_D(ModelParams)
    if checkD:
        RpRsSQ = get_RpRsSQ(ModelParams)
        for el in RpRsSQ:
            vfraction = el/(ModelParams['tT']['value']*ModelParams['tG']['value'])
            if vfraction < 0:
                bound = False

    return bound
            
def bound_bfraction_withD_2010(ModelParams):
    """ checks if b > 0 """

    bound = True
    checkD = bound_D(ModelParams)
    if checkD:
        RpRsSQ = get_RpRsSQ(ModelParams)
        for el in RpRsSQ:
            bfraction = 1e0 - np.sqrt(el)*(ModelParams['tT']['value']/ModelParams['tG']['value'])
            if bfraction < 0:
                bound = False

    return bound

def get_RpRsSQ_2010(ModelParams):
    
    RpRsSQ = []
    p = np.zeros(8)
    for par in ModelParams.keys():
        if par.startswith('D.'):
            splitD = map(str,par.split('.'))
            tag = ''
            for i in range(len(splitD)-1):
                tag = tag+'.'+splitD[i+1]
            v1 = ModelParams['v1'+tag]['value']
            v2 = ModelParams['v2'+tag]['value']
            p[0] = ModelParams['tT']['value']
            p[1] = ModelParams['tG']['value']
            p[2] = ModelParams[par]['value']
            p[3] = (v1 + v2)/2e0
            p[4] = (v1 - v2)/2e0
            a5 = -1.0e0*(p[3]+2.0e0*p[4])/(p[4]*np.sqrt(p[0]/p[1]))
            a4 = -1.0e0*(1.0e0-p[3]-p[4])/(p[4]*p[0]/p[1])
            a0 = p[2]*(1e0-p[3]/3e0-p[4]/6e0)/(p[4]*p[0]/p[1])
            RpRs = (tqe.newtraph6(0.3,a5,a4,a0))**2e0
            RpRsSQ.append(RpRs**2)

    return RpRsSQ

def bound_a0(ModelParams):
     """Checks if a0 > -50"""
     
     bound = True
     if ModelParams['a0']['value'] < -50e0:
        bound = False

     return bound

def bound_a1plusa2sq(ModelParams):
     """Checks if 0 < a1 + (a2**2) < 50 """
     
     bound = True
     combination = ModelParams['a1']['value'] + ModelParams['a2']['value']**2
     if  combination < 0e0 or combination > 50e0:
         bound = False

     return bound

