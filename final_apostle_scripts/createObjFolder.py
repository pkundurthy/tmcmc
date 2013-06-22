#!/astro/apps/pkg/python64/bin/python

import os
import sys
import optparse
import cPickle as pickle
from tmcmc import class_fitprep as cfp

MainPath = cfp.MainPath
ObjectList = cfp.ObjectList

def createFolder(ObjectName,fitType):
    """                         """
    
    ObjPath = MainPath+ObjectName+'/'
    
    if not os.path.exists(ObjPath):
        print 'making '+ObjPath
        os.makedirs(ObjPath)
    if not os.path.exists(ObjPath+'data/'):
        print 'making '+ObjPath+'data/'
        os.makedirs(ObjPath+'data/')
    if not os.path.exists(ObjPath+'data_detrended/'):
        print 'making '+ObjPath+'data_detrended/'
        os.makedirs(ObjPath+'data_detrended/')
        
    if fitType == 'mcmc':
        FolderList = [ObjPath+'MCMC.FLD/',\
                      ObjPath+'MCMC.OLD/',\
                      ObjPath+'MCMC.MDFLD/']
    elif fitType == 'minuit':
        FolderList = [ObjPath+'MINUIT.FLD/',\
                      ObjPath+'MINUIT.OLD/',\
                      ObjPath+'MINUIT.MDFLD/',\
                      ObjPath+'MINUIT.FIRSTTRY/']
    elif fitType == 'tap':
        if ObjectName.upper() == 'WASP2' \
        or ObjectName.upper() == 'XO2':
            FolderList = [ObjPath+'TAP.IBAND/',\
                          ObjPath+'TAP.RBAND/']
        else:
            FolderList = [ObjPath+'TAP.RBAND/']
    elif fitType == 'centriod':
        FolderList = [ObjPath+'CENTRIOD/']
    else:
        pass
    
    for FolderName in FolderList:
        if not os.path.exists(FolderName):
            print 'making '+FolderName
            os.makedirs(FolderName)

if __name__ == '__main__':
    
    if len(sys.argv) == 1:
        ObjectName = ' '
    else:
        ObjectName = sys.argv[1]
        
    if ObjectName not in ObjectList:
        print 'could not recognize object...'
        raise NameError('Unrecognized object')

    parser = optparse.OptionParser(usage=\
             "%prog ObjectName [mandatory] [optional folder condition]")

    parser.add_option('-a','--all',\
                      action='store_true',\
                      dest = 'allCondition',\
                      default = False,\
                      help = 'creates all fit conditions TAP, MCMC, MINIUT, CENTRIOD'\
                      )
    parser.add_option('-m','--mcmc',\
                      action='store_true',\
                      dest = 'MCMCCondition',\
                      default = False,\
                      help = 'creates all MCMC folders'\
                      )
    parser.add_option('-n','--minuit',\
                      action='store_true',\
                      dest = 'MINUITCondition',\
                      default = False,\
                      help = 'creates all requried MINIUT folders'\
                      )
    parser.add_option('-c','--centriod',\
                      action='store_true',\
                      dest = 'CENTRIODCondition',\
                      default = False,\
                      help = 'creates all requried Centriod folders'\
                      )
    parser.add_option('-t','--tap',\
                      action='store_true',\
                      dest = 'TAPCondition',\
                      default = False,\
                      help = 'creates all requried TAP folders'\
                      )

    (opts,args) = parser.parse_args()

    if opts.allCondition:
        opts.MCMCCondition = True
        opts.MINUITCondition = True
        opts.CENTRIODCondition = True
        opts.TAPCondition = True
    else:
        print 'folder creation not specified...'
        print parser.usage

    if opts.MCMCCondition:
        createFolder(ObjectName,'mcmc')
    if opts.MINUITCondition:
        createFolder(ObjectName,'minuit')
    if opts.CENTRIODCondition:
        createFolder(ObjectName,'centriod')
    if opts.TAPCondition:
        createFolder(ObjectName,'tap')
