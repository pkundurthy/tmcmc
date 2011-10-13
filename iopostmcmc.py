
from iomcmc import ReadHeaderMCMC, ReadMCMCline, ReadDetrendFile
from iomcmc import PrintModelParams, ReadStartParams
from mcmc import DetrendData
import numpy as np
import scipy
import sys

def readStatHeaders(FileName):
    """
        read the column and row parameter names from stat file
    """
    
    fileObj = open(FileName,'r')
    fileObj = fileObj.readlines()
    
    fileObj[0].strip('#')
    col = map(str,fileObj[0].strip('#').split())
    row = []
    
    for line in fileObj:
        if not line.startswith('#'):
            tag = map(str,line.split('|'))
            row.append(tag[0].strip())

    return col, row
            
def readStatsFile(FileName):
    """
    
    """
    
    ColN, RowN = readStatHeaders(FileName)
    fileObj = open(FileName,'r')
    fileObj = fileObj.readlines()
    
    i = 0
    Dict = {}
    for line in fileObj:
        if not line.startswith('#'):
            Fsplit = map(str, line.split('|'))
            Dsplit = map(float, Fsplit[1].split())
            Dict[RowN[i]] = dict(id=i)
            kvp = []
            for j in range(len(Dsplit)):
                kvp.append( (ColN[j],{'id':j,'value':Dsplit[j]}) )
            Dict[RowN[i]].update(dict(kvp))
            i += 1
    
    return Dict
    
def readALLStats(**kwargs):
    """
        read data from stats files
    """

    fileList = {}
    if len(kwargs) > 0:
        for key in kwargs:
            if key.lower().startswith('cov'):
                fileList['cov'] = kwargs[key]
            elif key.lower().startswith('spear'):
                fileList['spear'] = kwargs[key]
            elif key.lower().startswith('pear'):
                fileList['pear'] = kwargs[key]
            else:
                print 'No file identified for ', key
    else:
        print 'No keywords supplied '

    Stats = {}
    for fileKey in fileList.keys():
        if fileKey == 'cov':
            Stats['cov'] = readStatsFile(fileList[fileKey])
        elif fileKey == 'spear':
            Stats['spear'] = readStatsFile(fileList[fileKey])
        elif fileKey == 'pear':
            Stats['pear'] = readStatsFile(fileList[fileKey])
        else:
            pass
    
    return Stats

def isNonParam(key):
    """
        checks if a given MCMC data key is not a model parameter.
    """
    
    if key == 'acr' or key == 'frac' or key == 'chi1'\
    or key == 'chi2' or key == 'istep':
        return True
    else:
        return False

def getNparams(hdrkeys):
    """ reports the number of model parameters in the MCMC file """
    
    Nparam = 0
    for key in hdrkeys.keys():
        if isNonParam(key):
            pass
        else:
            Nparam += 1
            
    return Nparam

def readMCMChdr(filename):
    """ reads the header line for an mcmc file """
    
    mcmcFile = open(filename,'r')
    mcmcFile = mcmcFile.readlines()
    
    if mcmcFile[0].startswith('#'):
        hdrkeys = ReadHeaderMCMC(mcmcFile[0])
        for key in hdrkeys:
            hdrkeys[key] = hdrkeys[key].strip('\'')
    else:
        print 'Error: First line in %s is not the header' % filename
        sys.exit(1)

    return hdrkeys

def getPars(filename):
    """ return list of parameters only """
    
    HDRs = readMCMChdr(filename)
    ParList = []
    for key in HDRs.keys():
        if not isNonParam(HDRs[key]):
            ParList.append(HDRs[key])
    
    return ParList

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
            data_line = ReadMCMCline(line,hdrkeys)
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
            data_line = ReadMCMCline(line,hdrkeys)
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
            data_line = ReadMCMCline(line,hdrkeys)
            if Nparams == 1:
                if data_line['acr'] > 0.44-cropperc and data_line['acr'] < 0.44+cropperc:
                    print 'printing ',format(data_line['istep'],'n'),' acr ',data_line['acr']
                    print >> outfileObject, line.strip('\n')
            if Nparams > 1:
                if data_line['acr'] > 0.23-cropperc and data_line['acr'] < 0.23+cropperc:
                    print 'printing ',format(data_line['istep'],'n'),' acr ',data_line['acr']
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
    
    ModelParams = ReadStartParams(SampleParamFile)
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

    PrintModelParams(ModelParams,OutputParamFile)

def printErrors(MCMCfile,BestfitFile,OutputFile):
    """ Gets data out from the MCMC data file and the BESTFIT parameters file and prints uncertainties """

    mcmcData = readMCMC(MCMCfile)
    BestFitParams = ReadStartParams(BestfitFile)
    
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
    
def readDTfile(file,NuisONOFF):
    """
    read DT coefficients file.
    """
    
    NuisanceData = ReadDetrendFile(NuisONOFF)
    fileObj = open(file,'r')
    fileLines = fileObj.readlines()
    
    itag = 0
    TagList = []
    DTco = {}
    istep = 0
    for j in range(len(fileLines)):
        line = fileLines[j]
        if line.startswith('##'):
            line_header = map(str,line.split(']'))
            tag = line_header[0].strip('#').strip().strip('[')
            tag = tag.strip()
            parTags = map(str,line_header[1].strip(':\n').split('|')[:-2])
            if len(TagList) == 0:
                Tag0 = tag
            if tag == Tag0:
                istep += 1
                DTco[istep-1] = {}
            if tag not in TagList:
                itag += 1
                TagList.append(tag)
            line_data = map(str,fileLines[j+1].split(']'))
            tagCheck = line_data[0].strip('[')
            data = map(float,line_data[1].strip(':\n').split('|')[:-2])
            tagCheck = tagCheck.strip()
            if tagCheck != tag:
                print 'tags mismatched ', tagCheck, tag
                sys.exit(1)
            elif len(data) != len(parTags):
                print 'lengths mismatched ', len(data),len(parTags)
            else:
                pass
            kvp = []
            for i in range(len(parTags)):
                if parTags[i] in NuisanceData[tag]['dtparams'].keys():
                    kvp.append( (parTags[i],data[i]) )
            #print parTags
            #print NuisanceData[tag]['dtparams'].keys()
            #print kvp
            DTco[istep-1].update({tag:dict(kvp)})
             
    return DTco

def generateDT(MCMCFile,ObservedData,ModelParams,NuisanceData,FuncName):
    """
    Generate DT data from MCMCfile
    """
    
    exec "from myfunc import %s as ModelFunc" % FuncName
    
    DataMCMC = readMCMC(MCMCFile)
    DTco = {}
    for i in range(len(DataMCMC['istep'])):
        DTco[i] = {}
        for key in DataMCMC.keys():
            if not isNonParam(key):
                ModelParams[key]['value'] = DataMCMC[key][i]
        
        ModelData = ModelFunc(ModelParams,ObservedData)
        DetrendedData = DetrendData(ObservedData,ModelData,NuisanceData,'',False)
        
        for tag in DetrendedData.keys():
            if not tag.startswith('all'):
                DTco[i].update({tag:DetrendedData[tag]['dtcoeff']})
        
    return DTco

def correctionFromMCMC(MCMCFile,ObservedData,ModelParams,NuisanceData,FuncName):
    """
    Generate Correction functions from MCMCfile
    """
    
    exec "from myfunc import %s as ModelFunc" % FuncName
    
    DataMCMC = readMCMC(MCMCFile)
    DTco = {}
    for i in range(len(DataMCMC['istep'])):
        DTco[i] = {}
        for key in DataMCMC.keys():
            if not isNonParam(key):
                ModelParams[key]['value'] = DataMCMC[key][i]
        
        ModelData = ModelFunc(ModelParams,ObservedData)
        DetrendedData = DetrendData(ObservedData,ModelData,NuisanceData,'',False)
        
        for tag in DetrendedData.keys():
            if not tag.startswith('all'):
                DTco[i].update({tag:DetrendedData[tag]['correction']})
        
    return DTco

def correctionFromDTfile(file,NuisONOFF):
    """
    read DT coefficients and return correction function.
    """
    
    NuisanceData = ReadDetrendFile(NuisONOFF)
    fileObj = open(file,'r')
    fileLines = fileObj.readlines()
    
    itag = 0
    TagList = []
    DTco = {}
    istep = 0
    for j in range(len(fileLines)):
        line = fileLines[j]
        if line.startswith('##'):
            line_header = map(str,line.split(']'))
            tag = line_header[0].strip('#').strip().strip('[')
            tag = tag.strip()
            parTags = map(str,line_header[1].strip(':\n').split('|')[:-2])
            if len(TagList) == 0:
                Tag0 = tag
            if tag == Tag0:
                istep += 1
                DTco[istep-1] = {}
            if tag not in TagList:
                itag += 1
                TagList.append(tag)
            line_data = map(str,fileLines[j+1].split(']'))
            tagCheck = line_data[0].strip('[')
            data = map(float,line_data[1].strip(':\n').split('|')[:-2])
            tagCheck = tagCheck.strip()
            if tagCheck != tag:
                print 'tags mismatched ', tagCheck, tag
                sys.exit(1)
            elif len(data) != len(parTags):
                print 'lengths mismatched ', len(data),len(parTags)
            else:
                pass
            for i in range(len(parTags)):
                if i == 0:
                    Correction = \
                    np.zeros(len(NuisanceData[tag]\
                    ['dtparams'][parTags[i]]['data']))
                if parTags[i] != 'const':
                    Correction += data[i]*np.array(NuisanceData[tag]\
                    ['dtparams'][parTags[i]]['data'])
                
            #print parTags
            #print NuisanceData[tag]['dtparams'].keys()
            #print kvp
            DTco[istep-1].update({tag:Correction})
             
    return DTco
