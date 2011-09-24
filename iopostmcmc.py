

def readMCMChdr(filename):
    """ reads the header line for an mcmc file """
    
    mcmcFile = open(filename,'r')
    mcmcFile = mcmcFile.readlines()
    for line in mcmcFile:
        if line.startswith('#'):
            hdrkeys = mcmc.ReadHeaderMCMC(line)
            for key in hdrkeys:
                hdrkeys[key] = hdrkeys[key].strip('\'')

    return hdrkeys

def readMCMC(filename):
    """
        Reads data from an MCMC file and store it into a dictionary.
        INPUTS
            filename - file with MCMC data

        OUTPUTS
            data dictionary - with MCMC and related stats
    """

    out_data = {}
    hdrkeys = readMCMChdr(filename)
    for key in hdrkeys:
        out_data[hdrkeys[key]] = []
    
    mcmcFile = open(filename,'r')
    mcmcFile = mcmcFile.readlines()
    for line in mcmcFile:
        if not line.startswith('#'):
            data_line = mcmc.ReadMCMCline(line,hdrkeys)
            for key in data_line.keys():
                out_data[key].append(data_line[key])

    return out_data

def read1parMCMC(filename,parname):
    """
        Reads a single column of data from an MCMC file 
        and store it into a dictionary.
        INPUTS
            filename - file with MCMC data
            parname  - name of the parameter to be read
        OUTPUTS
            data dictionary - with MCMC and related stats
     """
     
    out_data = {}
    hdrkeys = readMCMChdr(filename)
    found = False
    for i in hdrkeys.keys():
        #print hdrkeys[i], parname
        if hdrkeys[i] == parname or hdrkeys[i] == 'istep' or hdrkeys[i] == 'chi1'\
        or hdrkeys[i] == 'acr' or hdrkeys[i] == 'frac':
            out_data[hdrkeys[i]] = []
            found = True
        else:
            continue

    if not found:
            print hdrkeys
            print 'Parameter ', parname, ' not found'
            sys.exit()
    
    mcmcFile = open(filename,'r')
    mcmcFile = mcmcFile.readlines()
    for line in mcmcFile:
        if not line.startswith('#'):
            data_line = mcmc.ReadMCMCline(line,hdrkeys)
            out_data[parname].append(data_line[parname])
            out_data['istep'].append(data_line['istep'])
            out_data['chi1'].append(data_line['chi1'])
            out_data['frac'].append(data_line['frac'])
            out_data['acr'].append(data_line['acr'])

    return out_data
            
def cropMCMC(mcmcfile,outfile,cropperc):
    """ Removes the "burn-in" phase of the MCMC and writes a 
    shortened MCMC data file 
    """
    
    hdrkeys = readMCMChdr(mcmcfile)
    Nparams = getNparams(hdrkeys)

    outfileObject = open(outfile,'w')
    mcmcfileobj = open(mcmcfile,'r')
    mcmcfileobj = mcmcfileobj.readlines()
    for line in mcmcfileobj:
        if line.startswith('#'):
            print >> outfileObject, line.strip('\n')
        if not line.startswith('#'):
            data_line = mcmc.ReadMCMCline(line,hdrkeys)
            if Nparams == 1:
                if data_line['acr'] > 0.44-cropperc and data_line['acr'] < 0.44+cropperc:
                    print 'printing ',format(data_line['istep'],'n')
                    print >> outfileObject, line.strip('\n')
            if Nparams > 1:
                if data_line['acr'] > 0.23-cropperc and data_line['acr'] < 0.23+cropperc:
                    print 'printing ',format(data_line['istep'],'n')
                    print >> outfileObject, line.strip('\n')

    outfileObject.close()
    
def makeStartFromExplore(ListOfChains,StablePerc,SampleParamFile,OutputParamFile):
    """
        Reads a list of single parameter step-exoploration chains 
        and prints a startparam file based on this data.
        This routine also prints whether a chain has stabilized
        the correct single-parameter acceptance rate.
    """
    
    ListFiles = open(ListOfChains,'r')
    ListFiles = ListFiles.readlines()
    
    ModelParams = mcmc.ReadStartParams(SampleParamFile)
    step = {}
    for file in ListFiles:
        data = readMCMC(file.strip('\n'))
        if data['acr'][-1] > 0.44-StablePerc and data['acr'][-1] < 0.44+StablePerc:
            for par in data.keys():
                if not isNonParam(par):
                    medfrac = np.median(data['frac'][-1000:])
                    print par+' has stabilized, acr = '+format(data['acr'][-1],'.2f')+' frac = '+str(medfrac)
                    step[par] = {'frac':medfrac}
        else:
            for par in data.keys():
                if not isNonParam(par):
                    print par+' has NOT stabilized, acr = '+format(data['acr'][-1],'.2f')

    for par in step.keys():
        for key in ModelParams.keys():
            if key == par:
                ModelParams[par]['step'] = ModelParams[par]['step']*step[par]['frac']
                ModelParams[par]['open'] = True

    mcmc.PrintModelParams(ModelParams,OutputParamFile)

def printErrors(MCMCfile,BestfitFile,OutputFile):
    """ Gets data out from the MCMC data file and the BESTFIT parameters file and prints uncertainties """

    mcmcData = readMCMC(MCMCfile)
    BestFitParams = mcmc.ReadStartParams(BestfitFile)
    
    erf15 = ((1e0 - scipy.special.erf(1e0/np.sqrt(2e0)))/2e0)
    erf84 = (1e0 - erf15)
    
    OutFileObject = open(OutputFile,'w')
    print >> OutFileObject, '#  Parameter   |  low15   | upp84  | use Single ?'
    for param in BestFitParams.keys():
        if BestFitParams[param]['open']:
            sort_list = sorted(mcmcData[param])
            Npoints = len(mcmcData[param])
            id84 = long(round(erf84*(Npoints-1)))
            id15 = long(round(erf15*(Npoints-1)))
            low15 = abs(BestFitParams[param]['value']-sort_list[id15])
            upp84 = abs(BestFitParams[param]['value']-sort_list[id84])
            if low15 >= upp84:
                greater = low15
                lower = upp84
            else:
                greater = upp84
                lower = low15
            useSingle = False
            if 1.1*lower >= 0.9*greater:
                useSingle = True
            print >> OutFileObject, param+'|'+\
            format(BestFitParams[param]['value'],BestFitParams[param]['printformat'])+'|'+\
            format(low15,BestFitParams[param]['printformat'])+'|'+\
            format(upp84,BestFitParams[param]['printformat'])+'|'+\
            str(useSingle)+'|:'

    OutFileObject.close()
