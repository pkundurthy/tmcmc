import minuit2
from mcmc import ApplyBounds, DetrendData
from iomcmc import PrintModelParams, ReadStartParams
import numpy as np
import cPickle as pickle
import sys
if sys.version_info[1] < 6:
    from tmcmc.misc import format

def MinuitPar2Err(ParFile,ErrFile):
    """ Convert a Minuit par file to an error file """
    
    ModelParams = ReadStartParams(ParFile)
    OutFile = open(ErrFile,'w')
    header = '# parname     |    value   | lower   | upper    | useSingle ?'
    print >> OutFile, header

    for par in ModelParams.keys():
        if par.lower() != 'reffilt':
            if ModelParams[par]['open']:
                ValString = format(ModelParams[par]['value'],ModelParams[par]['printformat'])
                ErrString = format(ModelParams[par]['step'],ModelParams[par]['printformat'])
                print >> OutFile, par+'|'+ValString+'|'+ErrString+'|'+ErrString+'| True '
            else:
                ValString = format(ModelParams[par]['value'],ModelParams[par]['printformat'])
                ErrString = 'nan'
                print >> OutFile, par+'|'+ValString+'|'+ErrString+'|'+ErrString+'| False '

    OutFile.close()

def RunMinuit(FunctionName,ObservedData,ModelParams,NuisanceData,BoundParams,tolnum,OutFile):
    """ Designed to run Minuit on tmcmc format Data dictionaries """
    
    OpenParNames = []
    for key in ModelParams.keys():
        if ModelParams[key]['open']:
            OpenParNames.append(key)
    startchi2 = f_chisquared(FunctionName,ObservedData,ModelParams,NuisanceData,BoundParams)
    dumpfile1 = open('dump1','wb')
    dumpfile2 = open('dump2','wb')
    dumpfile3 = open('dump3','wb')
    dumpfile4 = open('dump4','wb')
    dumpfile5 = open('dump5','wb')
    dumpfile6 = open('dump6','wb')
    pickle.dump(FunctionName,dumpfile1,-1)
    pickle.dump(ObservedData,dumpfile2,-1)
    pickle.dump(ModelParams,dumpfile3,-1)
    pickle.dump(NuisanceData,dumpfile4,-1)
    pickle.dump(BoundParams,dumpfile5,-1)
    pickle.dump(OpenParNames,dumpfile6,-1)
    dumpfile1.close()
    dumpfile2.close()
    dumpfile3.close()
    dumpfile4.close()
    dumpfile5.close()
    dumpfile6.close()

    # Begin running Minuit
    converge = False
    CountA1 = 0
    CountFail = 0
    AbsoluteFail = False
    while not converge:
        if CountFail > 20:
            print 'Failed'
            AbsoluteFail = True
            break
        try:
            m = minuit2.Minuit2(transit_chisquared(OpenParNames))
            m.tol = tolnum #55.4720096  #*1e8
            m.up = 1
            m.strategy = 2
            for key in m.values.keys():
                m.values[key] = ModelParams[key]['value']
                m.errors[key] = ModelParams[key]['step']
            m.migrad()
            #print 'edm = ',m.edm, '(edm < 1e-3 signifies convergence, edm > 1e2 is probably too high)'
            #print m.edm, converge, tolnum, 1e-3*m.tol*m.up, m.ncalls
            tolStatus = m.edm/(1e-3*m.tol*m.up)
            if tolStatus <= 1e0:
                if tolStatus == 1e0:
                    CountA1 = 100
                CountA1 += 1
                if CountA1 <= 4:
                    converge = False
                else:
                    converge = True
                tolnum *= tolStatus
                #CloseDict['a1'] = tolnum
                w = 'a1 Good Convergence'
            else:
                converge = False
                tolnum *= tolStatus
                w = 'a2 Poor Convergence'
                if np.isnan(tolStatus):
                    CountFail += 1 
            print tolStatus, m.edm, m.tol, tolnum, converge, w, CountFail
        except:
            if m.edm != None:
                edm = m.edm
            else:
                edm = 1e-2*m.tol*m.up
            if CountFail < 11:
                tolStatus = (edm/(1e-3*m.tol*m.up))
            elif CountFail > 11:
                tolStatus = (edm/(1e-3*m.tol*m.up))**(-1)
            else:
                tolStatus = 10e0/tolnum
            if tolStatus == 1.0:
                tolStatus = 10e0
            tolnum *= tolStatus
            converge = False
            CountFail += 1
            print tolStatus, m.edm, m.tol, tolnum, converge, 'b Failed Convergence', CountFail
            #raise

    for key in m.values.keys():
        ModelParams[key]['value'] = m.values[key]
        ModelParams[key]['step'] = m.errors[key]

    if not AbsoluteFail:
        DOF = len(ObservedData['all']['y']) - len(OpenParNames)
        PrintModelParams(ModelParams,OutFile)
        OutFileObjectAppend = open(OutFile,'a')
        print >> OutFileObjectAppend, \
        '# Best-fit ChiSQ = '+format(m.fval,'.2f')+' | Starting ChiSQ = ',format(startchi2,'.2f')
        print >> OutFileObjectAppend, '# DOF = '+format(DOF)
        print >> OutFileObjectAppend, \
        '# Best-fit reduced ChiSQ = '+format(m.fval/DOF,'.2f')+' | Starting reduced ChiSQ = '+format(startchi2/DOF,'.2f')
        OutFileObjectAppend.close()
    
def f_chisquared(FunctionName,ObservedData,ModelParams,NuisanceData,BoundParams):
    """ Computes chisquared the same way its done in the mcmc routines. """
    
    exec "from tmcmc.myfunc import %s as ModelFunc" % FunctionName
    withinbounds = ApplyBounds(ModelParams,BoundParams)
    if withinbounds:
        ModelData = ModelFunc(ModelParams,ObservedData)
        DetrendedData = DetrendData(ObservedData,ModelData,NuisanceData,'',False)
        mod = ModelData['all']['y']
        y = DetrendedData['all']['y']
        yerr = DetrendedData['all']['yerr']
        chi2 = np.sum( ((y-mod)/yerr)**2)
    else:
        chi2 = 1e308
        
    #print chi2
    return chi2

class var_code:
    def __init__(self, tdkeys):
        self.co_argcount = len(tdkeys)
        self.co_varnames = tuple(map(str, tdkeys))

class transit_chisquared:
    def __init__(self,parkeys):
        self.n = parkeys
        self.func_code = var_code(parkeys)
    def __call__(self,*args):
        #chi2 = 0e0
        dump1 = open('dump1','rb')
        dump2 = open('dump2','rb')
        dump3 = open('dump3','rb')
        dump4 = open('dump4','rb')
        dump5 = open('dump5','rb')
        dump6 = open('dump6','rb')
        FunctionName = pickle.load(dump1)
        ObservedData = pickle.load(dump2)
        ModelParams = pickle.load(dump3)
        NuisanceData = pickle.load(dump4)
        BoundParams = pickle.load(dump5)
        OpenParNames = pickle.load(dump6)
        for i in range(len(args)):
            ModelParams[OpenParNames[i]]['value'] = args[i]

        chi2 = f_chisquared(FunctionName,ObservedData,ModelParams,NuisanceData,BoundParams)
        #print len(args)
        return chi2