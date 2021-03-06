
from iopostmcmc import readMCMChdr
from iomcmc import ReadStartParams, ReadMCMCline
from iomcmc import PrintModelParams
from tqessential import LDC_v2u, computeRpRs
from tqessential import getTags, computePeriod
import MTQ_2011
import numpy as np
import os
import sys
if sys.version_info[1] < 6:
    from tmcmc.misc import format

def returnDerivedLine_MTQ2011(ModelParams,istep,keyList0):
    """ print a file with Derived parameters from the MCMC ensemble. """
        
    derived = {}
    
    Period = computePeriod(ModelParams)
    derived['Period'] = {'value':Period,'printformat':'.9f'}
    RefFilt = ModelParams['RefFilt']['printformat']

    # get Filter and Transit time tags
    Tags = getTags(ModelParams)
    
    # compute parameters used to compute lightcurve using the reference filter
    Dref, v1ref, v2ref = MTQ_2011.MTQ_FilterParams(RefFilt,Tags,ModelParams)
    u1ref, u2ref = LDC_v2u(v1ref,v2ref)

    tT = ModelParams['tT']['value']
    tG = ModelParams['tG']['value']
    
    TransitRef = MTQ_2011.MTQ_getDerivedParams(Dref,tT,tG,u1ref,u2ref,Period)
    #print TransitRef
    derived['inc'] = {'value':TransitRef['inc']*180e0/np.pi,'printformat':'.4f'}
    derived['b'] = {'value':TransitRef['b'],'printformat':'.6f'}
    derived['aRs'] = {'value':TransitRef['aRs'],'printformat':'.6f'}
    derived['velRs'] = {'value':TransitRef['velRs'],'printformat':'.6f'}
    derived['rho_star'] = {'value':TransitRef['rho_star'],'printformat':'.6f'}
    derived['RpRs'+'.'+ModelParams['RefFilt']['printformat']] = \
    {'value':TransitRef['RpRs'],'printformat':'.9f'}
    
    for key in ModelParams.keys():
        if key.startswith('T0'):
            split_TT = map(str,key.split('.'))
            transit_tag = split_TT[1].strip()
    
            # compute D, v1, v2 and then u1 and u2 for a given transit tag
            D, v1, v2 = MTQ_2011.MTQ_FilterParams(transit_tag,Tags,ModelParams)
            u1, u2 = LDC_v2u(v1,v2)
            RpRs = computeRpRs(u1,u2,tT,tG,D)
            filterD = filterMatchD(transit_tag,Tags,ModelParams)
            #print filterD
            derived['RpRs'+'.'+filterD] = {'value':RpRs,'printformat':'.9f'}
    
    DerivedLine = ''
    if istep == 0:
        keylist = derived.keys()
    else:
        keylist = keyList0

    Nkeys = len(keylist)
    if istep == 0:
        keyorder = {}
        for i in range(len(keylist)):
            keyorder[i] = keylist[i]
        for i in range(Nkeys):
            if i == 0:
                DerivedLine =\
                str(format(derived[keylist[i]]['value'],\
                derived[keylist[i]]['printformat']))
            else:
                DerivedLine =\
                DerivedLine+'|'+str(format(derived[keylist[i]]['value'],\
                derived[keylist[i]]['printformat']))
    else:
        for i in range(Nkeys):
            if i == 0:
                DerivedLine =\
                str(format(derived[keylist[i]]['value'],\
                derived[keylist[i]]['printformat']))
            else:
                DerivedLine = DerivedLine+'|'+str(format(derived[keylist[i]]['value'],\
                derived[keylist[i]]['printformat']))

    DerivedLine = DerivedLine+'|'+str(format(istep,'.0f'))+'|:'
    
    return DerivedLine, keylist

def printDerivedParFile_MTQ_2011(ParFile,OutParFile):
    """
    print the derived parameters in the format of the parameter file
    """
    
    ModelParams = ReadStartParams(ParFile)
    derived = {}
    
    Period = computePeriod(ModelParams)
    derived['Period'] = {'value':Period,'printformat':'.9f','open':True,'step':0.0}
    RefFilt = ModelParams['RefFilt']['printformat']

    # get Filter and Transit time tags
    Tags = getTags(ModelParams)
    
    # compute parameters used to compute lightcurve using the reference filter
    Dref, v1ref, v2ref = MTQ_2011.MTQ_FilterParams(RefFilt,Tags,ModelParams)
    u1ref, u2ref = LDC_v2u(v1ref,v2ref)

    tT = ModelParams['tT']['value']
    tG = ModelParams['tG']['value']
    
    TransitRef = MTQ_2011.MTQ_getDerivedParams(Dref,tT,tG,u1ref,u2ref,Period)
    #print TransitRef
    derived['inc'] = {'value':TransitRef['inc']*180e0/np.pi,'printformat':'.4f','open':True,'step':0.0}
    derived['b'] = {'value':TransitRef['b'],'printformat':'.6f','open':True,'step':0.0}
    derived['aRs'] = {'value':TransitRef['aRs'],'printformat':'.6f','open':True,'step':0.0}
    derived['velRs'] = {'value':TransitRef['velRs'],'printformat':'.6f','open':True,'step':0.0}
    derived['rho_star'] = {'value':TransitRef['rho_star'],'printformat':'.6f','open':True,'step':0.0}
    derived['RpRs'+'.'+ModelParams['RefFilt']['printformat']] = \
    {'value':TransitRef['RpRs'],'printformat':'.9f','open':True,'step':0.0}
    
    for key in ModelParams.keys():
        if key.startswith('T0'):
            split_TT = map(str,key.split('.'))
            transit_tag = split_TT[1].strip()
    
            # compute D, v1, v2 and then u1 and u2 for a given transit tag
            D, v1, v2 = MTQ_2011.MTQ_FilterParams(transit_tag,Tags,ModelParams)
            u1, u2 = LDC_v2u(v1,v2)
            RpRs = computeRpRs(u1,u2,tT,tG,D)
            filterD = filterMatchD(transit_tag,Tags,ModelParams)
            #print filterD
            derived['RpRs'+'.'+filterD] = {'value':RpRs,'printformat':'.9f','open':True,'step':0.0}
    
    PrintModelParams(derived,OutParFile)
    
def printDerived_MTQ_2011(STARTFILE,MCMCfile,DerivedFile):
    """ print a file with Derived parameters from the MCMC ensemble. """
    
    hdrKeys = readMCMChdr(MCMCfile)
    ModelParams = ReadStartParams(STARTFILE)
    
    mcmcFile = open(MCMCfile,'r')
    mcmcFile = mcmcFile.readlines()
    OutFileObject = open(DerivedFile,'w')
    
    for line in mcmcFile:
        derived = {}
        if not line.startswith('#'):
            data_line = ReadMCMCline(line,hdrKeys)
            print 'step/line = ',format(long(data_line['istep']),'n')
            for key in ModelParams.keys():
                if ModelParams[key]['open']:
                    ModelParams[key]['value'] = data_line[key]
            
            Period = computePeriod(ModelParams)
            derived['Period'] = {'value':Period,'printformat':'.9f'}
            RefFilt = ModelParams['RefFilt']['printformat']
    
            # get Filter and Transit time tags
            Tags = getTags(ModelParams)
            
            # compute parameters used to compute lightcurve using the reference filter
            Dref, v1ref, v2ref = MTQ_2011.MTQ_FilterParams(RefFilt,Tags,ModelParams)
            u1ref, u2ref = LDC_v2u(v1ref,v2ref)

            tT = ModelParams['tT']['value']
            tG = ModelParams['tG']['value']
            
            TransitRef = MTQ_2011.MTQ_getDerivedParams(Dref,tT,tG,u1ref,u2ref,Period)
            #print TransitRef
            derived['inc'] = {'value':TransitRef['inc']*180e0/np.pi,'printformat':'.4f'}
            derived['b'] = {'value':TransitRef['b'],'printformat':'.6f'}
            derived['aRs'] = {'value':TransitRef['aRs'],'printformat':'.6f'}
            derived['velRs'] = {'value':TransitRef['velRs'],'printformat':'.6f'}
            derived['rho_star'] = {'value':TransitRef['rho_star'],'printformat':'.6f'}
            derived['RpRs'+'.'+ModelParams['RefFilt']['printformat']] = \
            {'value':TransitRef['RpRs'],'printformat':'.9f'}
            
            for key in ModelParams.keys():
                if key.startswith('T0'):
                    split_TT = map(str,key.split('.'))
                    transit_tag = split_TT[1].strip()
            
                    # compute D, v1, v2 and then u1 and u2 for a given transit tag
                    D, v1, v2 = MTQ_2011.MTQ_FilterParams(transit_tag,Tags,ModelParams)
                    u1, u2 = LDC_v2u(v1,v2)
                    RpRs = computeRpRs(u1,u2,tT,tG,D)
                    filterD = filterMatchD(transit_tag,Tags,ModelParams)
                    #print filterD
                    derived['RpRs'+'.'+filterD] = {'value':RpRs,'printformat':'.9f'}
            
            DerivedLine = ''
            keylist = derived.keys()
            Nkeys = len(keylist)
            if data_line['istep'] == 0:
                keyorder = {}
                for i in range(len(keylist)):
                    keyorder[i] = keylist[i]
                for i in range(Nkeys):
                    if i == 0:
                        DerivedLine =\
                        str(format(derived[keylist[i]]['value'],\
                        derived[keylist[i]]['printformat']))
                    else:
                        DerivedLine =\
                        DerivedLine+'|'+str(format(derived[keylist[i]]['value'],\
                        derived[keylist[i]]['printformat']))
            else:
                for i in range(Nkeys):
                    if i == 0:
                        DerivedLine =\
                        str(format(derived[keylist[i]]['value'],\
                        derived[keylist[i]]['printformat']))
                    else:
                        DerivedLine = DerivedLine+'|'+str(format(derived[keylist[i]]['value'],\
                        derived[keylist[i]]['printformat']))

            DerivedLine = DerivedLine+'|'+str(format(data_line['istep'],'.0f'))+'|:'
            print >> OutFileObject, DerivedLine
    
    keyline = ''
    for i in range(Nkeys):
        if i == 0:
            keyline = '#'+keylist[i]
        else:
            keyline = keyline+'|'+keylist[i]
    keyline = keyline+'|istep|:'
    
    OutFileObject.close()
    
    #print >> OutFileObject, keyline
    opencopy = open(DerivedFile,'r')
    opencopy = opencopy.readlines()
    os.system('rm -v %s' % (DerivedFile))
    rearranged = open(DerivedFile,'w')
    print >> rearranged, keyline
    for iline in range(len(opencopy)):
        print >> rearranged, opencopy[iline].strip('\n')
    rearranged.close()

def filterMatchD(TransitTag,Tags,ModelParams):
    """
        Returns filter tag for depth
    """
    
    D = None
    for par in Tags.keys():
        if par.startswith('D'):
            FiltMatch_D = False
            if TransitTag == Tags[par]['Filter']:
                FiltMatch_D = True
            for TTags in Tags[par]['TT']:
                if TransitTag == TTags:
                    FiltMatch_D = True
            if FiltMatch_D:
                D = ModelParams[par]['value']
                return par.strip('D.')
