#!/astro/apps/pkg/python64/bin//python

import os
import sys
import tmcmc
import optparse
import class_fitprep as cfp

MainPath = cfp.MainPath
ObjectList = cfp.ObjectList

def fitprep_mkMM(ObjectName, fitName,fitNum):
    """                 """
    
    Object = cfp.Object(ObjectName)
    Object.InitiateCase(fitName)
    Object.InitiateFitNum(fitNum)
    
    Object.MakeBoundFile()
    Object.MakeStartFile(5)

if __name__ == '__main__':
    
    if len(sys.argv) == 1:
        ObjectName = ' '
    else:
        ObjectName = sys.argv[1]
    
    if ObjectName not in ObjectList:
        print 'could not recognize object...'
        raise NameError('Unrecognized object')

    parser = optparse.OptionParser(usage=\
             "%prog ObjectName [mandatory] [fit number]")

    parser.add_option('-f','--fit',\
                      dest = 'fitName',\
                      default = 'fail',\
                      help = 'start conditions (MCMC.FLD, MCMC.OLD MCMC.MDFLD)')
                      
    parser.add_option('-n','--num',\
                      dest = 'fitNum',\
                      default = 0,\
                      help = 'the fit number')

    (opts,args) = parser.parse_args()

    if opts.fitName.lower() == 'fail':
        parser.error('fit type not specified')
    
    if opts.fitNum == 0:
        parser.error('fit number not specified')
    
    fitprep_mkMM(ObjectName,opts.fitName,opts.fitNum)