import tqessential as tqe
import numpy as np

def MTQ_multidepth_tduration(ModelParams,ObservedData):
    """
    Computes model lightcurves given parameters and Observed times for multiple transits.
    
    Inputs - the tmcmc format 'ModelParams' dictionary and tmcmc format 'ObservedData' dictionary
    Output - the tmcmc format 'ModelData' dictionary
    """

    Period = tqe.computePeriod(ModelParams)
    RefFilt = ModelParams['RefFilt']['printformat']
    
    # get Filter and Transit time tags
    Tags = tqe.getTags(ModelParams)
    
    # compute parameters used to compute lightcurve using the reference filter
    Dref, v1ref, v2ref = MTQ_FilterParams(RefFilt,Tags,ModelParams)
    u1ref, u2ref = tqe.LDC_v2u(v1ref,v2ref)

    tT = ModelParams['tT']['value']
    tG = ModelParams['tG']['value']
    
    # compute 'b', 'i' and other parameters for the reference transit
    TransitRef = MTQ_getDerivedParams(Dref,tT,tG,u1ref,u2ref,Period)

    fmod = {}
    for key in ModelParams.keys():
        if key.startswith('T0'):
            # get the transit tag from a given transit time parameter
            split_TT = map(str,key.split('.'))
            transit_tag = split_TT[1].strip()
            
            # compute D, v1, v2 and then u1 and u2 for a given transit tag
            D, v1, v2 = MTQ_FilterParams(transit_tag,Tags,ModelParams)
            u1, u2 = tqe.LDC_v2u(v1,v2)
            
            # Compute various parameters for transit lightcurve
            F0 = ModelParams['f0']['value']
            timeIn = np.array(ObservedData[transit_tag]['x'])
            T0 = ModelParams['T0.'+transit_tag]['value']
            RpRs = tqe.computeRpRs(u1,u2,tT,tG,D)
            
            # Compute lightcurve
            fmodout = tqe.TransitLC(timeIn,F0,TransitRef['inc'],\
            TransitRef['aRs'],Period,RpRs,u1,u2,T0)
            fmod[transit_tag] = {'y':fmodout}

    # Stacking lightcurves from different nights
    all_fmodout = []
    Ntags = len(ObservedData['all']['tagorder'].keys())
    for tag in np.array(range(Ntags))+1:
        transit_tag = ObservedData['all']['tagorder'][tag]
        all_fmodout = np.hstack((all_fmodout,fmod[transit_tag]['y']))

    fmod['all'] = {'y':all_fmodout}
    return fmod

def MTQ_getDerivedParams(D,tT,tG,u1,u2,Period):
    """
        Computes a set of derived parameters and returns them in dictionary form.
        
        Inputs = Depth (D), transit duration (tT), ingress duration (tG)
        the limb-darkening coefficients (u1 and u2) and the period.
        Outputs = 'velRs' (v/Rstar), 'aRs' (a/Rstar), 'b', 'inc', 'rho_star'
        and 'RpRs' (Rp/Rstar).
    """
    
    # Parameters computed
    #print u1, u2, tG, tT, D
    P = Period*86400e0                       # Convert from days to seconds 
    G = 6.67259e-8                           # cm**3 g*-1 s**-2 (cgs)
    RpRs = tqe.computeRpRs(u1,u2,tT,tG,D)    # -
    velRs = 2e0*np.sqrt(RpRs/(tT*tG))        # day^-1
    aRs = Period*velRs/(2e0*np.pi)           # -
    rho_star = 3e0*np.pi*(aRs**3)/(G*(P**2)) # g cm**-3
    b = (np.sqrt(1e0-(tT/tG)*RpRs))          # -
    inc = np.arccos(b/aRs)                   # radians
    return {'velRs':velRs,'aRs':aRs,'b':b,'inc':inc,'rho_star':rho_star,'RpRs':RpRs}

def MTQ_FilterParams(RefFilt,Tags,ModelParams):
    """
        Matches D, v1 and v2 for a given filter and returns these values.
        
        Input = RefFilt (string with name of reference filter)
                Tags (dictionary separating filter tags and transit tags for given parameters)
                ModelParams
        
        Output = D, v1 and v2 (of a given filter)
    """
    
    D = None
    v1 = None
    v2 = None
    for par in Tags.keys():
        if par.startswith('D'):
            FiltMatch_D = False
            if RefFilt == Tags[par]['Filter']:
                FiltMatch_D = True
            for TTags in Tags[par]['TT']:
                if RefFilt == TTags:
                    FiltMatch_D = True
            if FiltMatch_D:
                D = ModelParams[par]['value']
        if par.startswith('v1'):
            FiltMatch_v1 = False
            #print RefFilt, Tags[par]['Filter']
            if RefFilt == Tags[par]['Filter']:
                FiltMatch_v1 = True
            for TTags in Tags[par]['TT']:
                if RefFilt == TTags:
                    FiltMatch_v1 = True
            if FiltMatch_v1:
                v1 = ModelParams[par]['value']
        if par.startswith('v2'):
            FiltMatch_v2 = False
            #print RefFilt, Tags[par]['Filter']
            if RefFilt == Tags[par]['Filter']:
                FiltMatch_v2 = True
            for TTags in Tags[par]['TT']:
                if RefFilt == TTags:
                    FiltMatch_v2 = True
            if FiltMatch_v2:
                v2 = ModelParams[par]['value']
    
    return D, v1, v2