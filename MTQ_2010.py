
import numpy as np
import tmcmc.tqessential as tqe
import sys
if sys.version_info[1] < 6:
    from tmcmc.misc import format

def MultiTransitQuick_circular_rprs_vm(ModelParams,ObservedData):
    """ Computes model lightcurves given parameters and Observed times for multiple transits. This _rprs_vm version is for fitting the planet-to-star radius ratio squared (Rp/Rs)**2. This is the version to use for multi-wavelength datasets. 'vm' indicated we are using the linear combination of the Mandel & Agol (2002) limb-darkening coefficients. 
    
    Inputs - the tmcmc format 'ModelParams' dictionary and tmcmc format 'ObservedData' dictionary
    Output - the tmcmc format 'ModelData' dictionary
    """

    p = np.zeros(8)
    fmod = {}
    out = []
    NTarr = []
    TTarr = []
    for pname in ModelParams.keys():
        if pname.startswith('T0'):
            mapname = map(str, pname.split('.'))
            if len(mapname) == 2:
                Nname = 'NT.'+mapname[1]
                TTarr.append(ModelParams[pname]['value'])
                NTarr.append(ModelParams[Nname.strip()]['value'])
            else:
                print 'string splitting error'
    
    if len(NTarr) == len(TTarr) and len(NTarr) > 1: 
        Period = tqe.slopefitquick(NTarr,TTarr)
    else:
        print 'ERROR: only 1 transit time detected'
        print 'ERROR: add at least one more transit time so that ephemeris may be computed'
        Period = 0
        sys.exit()
    
    for key in ModelParams.keys():
        if key.startswith('T0'):
            split_TT = map(str,key.split('.'))
            transit_tag = split_TT[1].strip()
            p[0] = ModelParams['tT']['value']
            p[1] = ModelParams['tG']['value']
            p[2] = ModelParams['RpRsSQ']['value']
            for keyalt in ModelParams.keys():
                if keyalt.startswith('v1'):
                    split_v1 = map(str,keyalt.split('.'))
                    for el in split_v1:
                        if el == transit_tag:
                            v1 = ModelParams[keyalt]['value']
                if keyalt.startswith('v2'):
                    split_v2 = map(str,keyalt.split('.'))
                    for el in split_v2:
                        if el == transit_tag:
                            v2 = ModelParams[keyalt]['value']
            p[3] = (v1+v2)/2e0
            p[4] = (v1-v2)/2e0
            p[5] = ModelParams['f0']['value']
            p[6] = Period
            timekey = str(key).strip()
            p[7] = ModelParams[timekey]['value']
            #print timekey, transit_tag
            tin = np.array(ObservedData[transit_tag]['x'])
            fmodout= transitquick_circ_rprs(tin,p)
            fmod[transit_tag] = {'y':fmodout}
    
    all_fmodout = []
    Ntags = len(ObservedData['all']['tagorder'].keys())
    for tag in np.array(range(Ntags))+1:
            transit_tag = ObservedData['all']['tagorder'][tag]
            all_fmodout = np.hstack((all_fmodout,fmod[transit_tag]['y']))
      
    fmod['all'] = {'y':all_fmodout}
    return fmod

def MultiTransitQuick_circular_depth_vm(ModelParams,ObservedData):
    """ Computes model lightcurves given parameters and Observed times for multiple transits. This _rprs_vm version is for the transit depth 'D' (see Kundurthy et al. 2011). Useful for single wavelength datasets. 'vm' indicates we are using the linear combination of the Mandel & Agol (2002) limb-darkening coefficients. 
    
    Inputs - the tmcmc format 'ModelParams' dictionary and tmcmc format 'ObservedData' dictionary
    Output - the tmcmc format 'ModelData' dictionary
    """
    
    p = np.zeros(8)
    fmod = {}
    out = []
    NTarr = []
    TTarr = []
    for pname in ModelParams['par'].keys():
        if pname.startswith('T0'):
            mapname = map(str, pname.split('.'))
            if len(mapname) == 2:
                Nname = 'NT.'+mapname[1]
                TTarr.append(ModelParams[pname]['value'])
                NTarr.append(ModelParams[Nname.strip()]['value'])
            else:
                print 'string splitting error'

    if len(NTarr) == len(TTarr) and len(NTarr) > 1: 
        Period = tqe.slopefitquick(NTarr,TTarr)
    else:
        print 'ERROR: only 1 transit time detected'
        print 'ERROR: add at least one more transit time so that ephemeris may be computed'
        Period = 0
        sys.exit()

    for key in ModelParams.keys():
        if key.startswith('T0'):
            split_TT = map(str,key.split('.'))
            transit_tag = split_TT[1].strip()
            p[0] = ModelParams['tT']['value']
            p[1] = ModelParams['tG']['value']
            p[2] = ModelParams['D']['value']
            for keyalt in ModelParams.keys():
                if keyalt.startswith('v1'):
                    split_v1 = map(str,keyalt.split('.'))
                    for el in split_v1:
                        if el == transit_tag:
                            v1 = ModelParams[keyalt]['value']
                if keyalt.startswith('v2'):
                    split_v2 = map(str,keyalt.split('.'))
                    for el in split_v2:
                        if el == transit_tag:
                            v2 = ModelParams[keyalt]['value']
            p[3] = (v1+v2)/2e0
            p[4] = (v1-v2)/2e0
            p[5] = ModelParams['f0']['value']
            p[6] = Period
            timekey = str(key).strip()
            p[7] = ModelParams[timekey]['value']
            tin = np.array(ObservedData[transit_tag]['x'])
            fmodout= transitquick_circ_depth(tin,p)
            fmod[transit_tag] = {'y':fmodout}
    
    all_fmodout = []
    Ntags = len(ObservedData['all']['tagorder'].keys())
    for tag in np.array(range(Ntags))+1:
            transit_tag = ObservedData['all']['tagorder'][tag]
            all_fmodout = np.hstack((all_fmodout,fmod[transit_tag]['y']))

    fmod['all'] = {'y':all_fmodout}
    return fmod

def transitquick_circ_depth(t,p):
    """ The python translation of transitquick.pro. Computes a transit lightcurve as a
        function of time, t, usually in HJD or BJD.
 
      Input parameters (x) are:
      p[0] = tT = transit duration in days
      p[1] = tG = ingress/egress duration in days
      p[2] = D = (R_p/R_*)^2 * I(b)/I(0)= transit depth
      p[3] = u1 = linear limb-darkening parameter
      p[4] = u2 = quadratic limb-darkening coefficient
      p[5] = F0 = uneclipsed flux
      p[6] = Period = calculated in multi_transitquick
      p[7] = T0.TN = Transit time
    """
    
    a5 = -1.0e0*(p[3]+2.0e0*p[4])/(p[4]*np.sqrt(p[0]/p[1]))
    a4 = -1.0e0*(1.0e0-p[3]-p[4])/(p[4]*p[0]/p[1])
    a0 = p[2]*(1e0-p[3]/3e0-p[4]/6e0)/(p[4]*p[0]/p[1])
    RpRs = (tqe.newtraph6(0.3,a5,a4,a0))**2e0
    th = (2e0*np.pi/p[6])*(t-p[7])
    vel = 2e0*np.sqrt(RpRs/(p[0]*p[1]))
    aRs = p[6]*vel/(2e0*np.pi)
    b = (np.sqrt(1e0-(p[0]/p[1])*RpRs))
    inc = np.arccos(b/aRs)

    z0 = aRs*np.sqrt(1e0 - (np.cos(th)*np.sin(inc))**2e0)
    out = tqe.occultquad(z0,p[3],p[4],RpRs)
    flux= out[:][0]*p[5]
    #print RpRs, vel, aRs, b, inc, a5, a4, a0
    return flux

def transitquick_circ_rprs(t,p):
    """ Computes a transit lightcurve, normalized to unity, as a
     function of time, t, usually in HJD or BJD.

     Input parameters (x) are:
     p[0] = tT = transit duration in days
     p[1] = tG = ingress/egress duration in days
     p[2] = RpRsSQ = (R_p/R_*)^2 ~ transit depth
     p[3] = u1 = linear limb-darkening parameter
     p[4] = u2 = quadratic limb-darkening coefficient
     p[5] = F0 = uneclipsed flux
     p[6] = Period = calculated in multi_transitquick
     p[7] = T0.TN = Transit time
     """
    
    RpRs = np.sqrt(p[2])
    th = (2e0*np.pi/p[6])*(t-p[7])
    vel = 2e0*np.sqrt(RpRs/(p[0]*p[1]))
    aRs = p[6]*vel/(2e0*np.pi)
    b = (np.sqrt(1e0-(p[0]/p[1])*RpRs))
    inc = np.arccos(b/aRs)

    z0 = aRs*np.sqrt(1e0 - (np.cos(th)*np.sin(inc))**2e0)
    out = tqe.occultquad(z0,p[3],p[4],RpRs)
    flux= out[:][0]*p[5]
    #print RpRs, vel, aRs, b, inc, a5, a4, a0
    return flux
