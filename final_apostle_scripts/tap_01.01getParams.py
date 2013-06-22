#!/astro/apps/pkg/python64/bin//python

import tmcmc
from tmcmc import class_fitprep as cfp
import sys

def print_TAP_Params(ObjectName):
    """                 """
    
    Object = cfp.Object(ObjectName)
    Object.InitiateTAP()
    Object.printTAP_Output()

if __name__ == '__main__':
    
    ObjectName = sys.argv[1]
    print_TAP_Params(ObjectName)
