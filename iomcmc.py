
from tmcmc.misc import String2IntFloat
from tmcmc.misc import String2Bool

import os, sys
if sys.version_info[1] < 6:
    from tmcmc.misc import format
    
def MakeModelParsContinue(par0,par1,ModelPars):
    """ Makes a ModelParam dictionary from lines of an incompelte MCMC file."""

    newModelPars = {}
    for key in ModelPars.keys():
        if ModelPars[key]['open']:
            newModelPars[key] = {'value':par1[key],'step':(par1[key]-par0[key])/par1['frac'],\
            'open':ModelPars[key]['open'],'printformat':ModelPars[key]['printformat']}
        else:
            newModelPars[key] = {'value':ModelPars[key]['value'],'step':ModelPars[key]['step'],\
            'open':ModelPars[key]['open'],'printformat':ModelPars[key]['printformat']}

    return newModelPars


def ReadStartParams(filename):
    """ Returns a dictionary containing parameters and associated data.
        Parameter files must be in the following form
        col 1 = Parameter Name (string) | col 2 = Parameter Value  (float) |
        col 3 = Stepsize (float) | col 4 = Open/Close Flag (Bool) | col 5 =
        printformating (string)
        Lines starting with '#' are treated as comments and skipped.
    """
    
    file_object = open(filename,'r')
    file_object = file_object.readlines()
    count = 0
    par = {}

    for line in file_object:
        if not line.startswith('#'):
            dummy_array = map(str,line.split('|'))
            count += 1
            try:
                par[dummy_array[0].strip()] = {'value':float(dummy_array[1]),'step':float(dummy_array[2]),\
                'open':String2Bool(dummy_array[3].strip()),'printformat':dummy_array[4].strip()}
            except:
                par[dummy_array[0].strip()] = {'value':str(dummy_array[1]),'step':float(dummy_array[2]),\
                'open':String2Bool(dummy_array[3].strip()),'printformat':dummy_array[4].strip()}

    # print str(count)+' Parameters read'
    if count > 200:
        print 'You might have too many parameters'
        sys.exit()
    return par

def ReadSingleDataFile(file):
    """ Returns a dictionary pf x,y,yerr data after reading a generic data file.
        Data file should have the following form:
        col 1 = x (abscissa) | col 2 = y (ordinate)  | col 3 = yerr (error in ordinate)
        Lines starting with '#' are treated as comments and skipped.
    """
    
    file_object = open(file,'r')
    file_object = file_object.readlines()
    data_point_count = 0
    
    # Empty arrays for data
    x=[]
    y = []
    yerr = []
    data_out = {}

    for line in file_object:
        if not line.startswith('#'):
            dummy_array = map(str,line.split('|'))
            data_point_count += 1
            x.append(float(dummy_array[0]))
            y.append(float(dummy_array[1]))
            yerr.append(float(dummy_array[2]))

    data_out['all'] = {'x':x,'y':y,'yerr':yerr}
    # print str(data_point_count)+' data points read'
    return data_out

def ReadDataFile(file):
    """ Returns a dictionary of observerd transit (or other) data, read from a single file.
        Data file should have the following form:
        col 1 = t (time stamp or x values) | 
        col 2 = Fobs (normalized flux ratio or y values = observed data)  | 
        col 3 = errFobs (error in normalized flux ratio or errors in y observed)
        Lines starting with '#' are treated as comments and skipped.
    """
    
    file_object = open(file,'r')
    file_object = file_object.readlines()
    data_point_count = 0
        # Empty arrays for data
    x=[]
    y = []
    yerr = []
    data_out = {}

    for line in file_object:
        if not line.startswith('#'):
            dummy_array = map(str,line.split('|'))
            data_point_count += 1
            x.append(float(dummy_array[0]))
            y.append(float(dummy_array[1]))
            yerr.append(float(dummy_array[2]))

    data_out = {'x':x,'y':y,'yerr':yerr}
            
    # print str(data_point_count)+' data points read'
    return data_out

def ReadMultiList(listfile):
    """ Returns a dictionary with observed data after reading a data file list.
        Data file should have the following form:
        col 1 = path/filename  | col 2 = transit tag (or other tag)
        Lines in datafile starting with '#' are treated as comments and skipped.
    """
    
    file_object = open(listfile,'r')
    file_object = file_object.readlines()
    data_point_count = 0
    # Empty arrays for data
    data_out = {}

    for line in file_object:
        if not line.startswith('#'):
            dummy_array = map(str,line.split('|'))
            # arr[0] should be a single transit data filename.
            # arr[1] should be the associated transit tag.
            data_point_count += 1
            single_set_data = ReadDataFile(dummy_array[0].strip())
            tag = dummy_array[1].strip().strip('\n')
            data_out[tag] = single_set_data

    # Lists for time-stamps, flux ratios and errors to be appended with data from all lightcurves.
    x_all = []
    yobs_all = []
    yerr_all = []
    tagorder = {}
    sequence = 0
    for set_tag in data_out.keys():
        x_all.extend(data_out[set_tag]['x'])
        yobs_all.extend(data_out[set_tag]['y'])
        yerr_all.extend(data_out[set_tag]['yerr'])
        sequence += 1
        tagorder[sequence] = set_tag

    data_out['all'] = {'x':x_all,'y':yobs_all,'yerr':yerr_all,'tagorder':tagorder}

    return data_out

def ReadColFloat(file,separator,comment):
    """ Reads data in column separated format into a float list."""
    
    file = open(file,'r')
    file = file.readlines()
    out_list = []
    flag_check = 0
    for line in file:
        if not line.startswith(comment):
            dummy_array = map(float,line.split(separator))
            if flag_check == 0:
                # Check the number of columns of data and make an empty list to match.
                ncols = len(dummy_array)
                for i in range(ncols): 
                    out_list.append([])
            flag_check = 1 # Populate list with data after check.
            for i in range(ncols):
                out_list[i].append(dummy_array[i]) 
    return out_list

def checkFileExists(file):
    exists = os.path.isfile(file)
    if exists:
        full = bool(os.stat(file)[6])
        if not full:
            exists = False
    return exists

def ReadDetrendFile(file):
    """ Returns a dictionary with collected detrending data.
        Data file should have the following form:
        col1 = Detrending File Path | col 2 = Transit Tag | col 3 = Flag for Nuisance parameter 1...
        and each subsequent column lists a detrending parameter beyond that.
        The first line with comments is used to read the names of nuisance parameters.
    """
    
    file_object = open(file,'r')
    file_object = file_object.readlines()
    headercount = 0
    var_name = []
    detrend_out = {}
    atLeastOneTrue = False
    # Obtain the list of strings containing variable names.
    for line in file_object:
        if line.startswith('#'):
            headercount += 1
            if headercount == 1:
                dummy_array = map(str,line.split('|'))
                for el in dummy_array:
                    var_name.append(el.strip())

    #print var_name
    var_name = var_name[2:]   # Getting rid of names that are not nuisance params.
    #print var_name
    #for i in range(len(var_name)): var_name[i].strip()   # Getting rid of spaces in remaining names.

    for line in file_object:
        if not line.startswith('#'):
            dummy_array = map(str, line.split('|'))
            NuisanceFile = dummy_array[0].strip()       # arr[0] should have the filename string
            TransitTag = dummy_array[1].strip()
            #print 'Reading detrending data from ', NuisanceFile
            flags_whole = dummy_array[2:]
            flags_int = []
            flags = []
            for element in flags_whole:
                flags_int.append(String2IntFloat(element.strip()))
            for element in flags_int:
                if element == 1: flags.append(True)
                if element == 0: flags.append(False)
                if element != 0 and element != 1:
                    print 'Error in ON/OFF Flags', el, line
                    sys.exit()
            if len(flags) == len(var_name):
                data_detrend = ReadColFloat(NuisanceFile,'|','#')
                parameters = {}
                for i in range(len(var_name)):
                    if flags[i] == False:
                        parameters[var_name[i]] = {'used':flags[i],'data':[]}
                    if flags[i] == True:
                        if not atLeastOneTrue: atLeastOneTrue = True
                        if len(data_detrend) == 0:
                            parameters[var_name[i]] = {'used':False,'data':[]}
                        else:
                            parameters[var_name[i]] = {'used':flags[i],'data':data_detrend[:][i]}
                detrend_out[TransitTag] = {'filename':NuisanceFile,'dtparams':parameters}
            else:
                print 'tags do not match var_name'
                print len(flags), len(var_name)
                print flags, var_name

    detrend_out['GlobalSwitch'] = atLeastOneTrue
    return detrend_out

def ReadBoundsFile(file):
    """ Returns a dictionary with information on bounds.
        Data file should have the following form:
        col1 = Bounds Function String | col 2 = Apply Bounds Flag
        Lines in datafile starting with '#' are treated as comments and skipped.
    """
    
    file_object = open(file,'r')
    file_object = file_object.readlines()

    BoundPar = {}
    for line in file_object:
        if not line.startswith('#'):
            dummy_array = map(str, line.split('|'))
            BoundPar[dummy_array[0].strip()] = {'open':String2Bool(dummy_array[1].strip())}
            # arr[0] is the function name/tag
            # arr[1] is the flag that describes whether the bounds are open or closed

    return BoundPar

def ReadHeaderMCMC(line):
    """ Reads a commented line in an MCMC and outputs parameter names."""

    line = line.strip('#').strip('|:\n\n')
    name_array = map(str,line.split('|'))
    par_out = {}
    for i in range(len(name_array)):
        par_out[i] = name_array[i].strip()
        
    return par_out

def ReadMCMCline(line,header):
    """ Reads a line of MCMC data. """

    line = line.strip('|:\n\n')
    name_array = map(float,line.split('|'))
    par_out = {}
    for key in header.keys():
        par_out[header[key]] = name_array[int(key)]

    return par_out

def WriteLowestChisq(file,ModelParams,OutFileName,ShowOutput):
    """ Finds the lowest chisq point in MCMC and prints to a file
        of format similar to the start paramfile.
        Inputs 
            file - the MCMC file
            ModelPars
            OutFileName
        Output
            a file with OutFileName
    """
    
    ModelParamsCopy = {}
    
    if checkFileExists(file):
        FileObject = open(file,'r')
        FileObjectLines = FileObject.readlines()
        minchi = 1e308
        for line in FileObjectLines:
            if line.startswith('#'):
                ParNames = ReadHeaderMCMC(line)
            else:
                if line.endswith("|:\n"):
                    par0 = ReadMCMCline(line,ParNames)
                    if par0['chi1'] < minchi:
                        minchi = par0['chi1']
                        if ShowOutput: print 'Lowest chisq = ',format(minchi,'.2f'),\
                        ' @ step = ',format(par0['istep'],'n')
                        for key in ModelParams.keys():
                            if ModelParams[key]['open']:
                                ModelParamsCopy[key] = {'value':par0[key],'step':ModelParams[key]['step'],\
                                'printformat':ModelParams[key]['printformat'],'open':ModelParams[key]['open']}
                            else:
                                ModelParamsCopy[key] = {'value':ModelParams[key]['value'],'step':\
                                ModelParams[key]['step'],'printformat':ModelParams[key]\
                                ['printformat'],'open':ModelParams[key]['open']}
                    else:
                        pass
        PrintModelParams(ModelParamsCopy,OutFileName)
    else:
        print file, ' does not exist.'

def CheckContinue(file,ModelPars):
    """ Checks an MCMC outfile for continuation. """

    FileObject = open(file,'r')
    FileObjectLines = FileObject.readlines()
    
    CopyFile = file+'.COPY'
    ContinueFile = file+'.CONTINUE'
    OutFile = open(CopyFile,'w')
    if checkFileExists(ContinueFile):
        OutFileContinueStep = open(ContinueFile,'a')
    else:
        OutFileContinueStep = open(ContinueFile,'w')

    ReadLines = []

    for line in FileObjectLines:
        if line.startswith('#'):
            ParNames = ReadHeaderMCMC(line)
            print >> OutFile, line.strip('\n\n')
        else:
            if line.endswith("|:\n"):
                print >> OutFile, line.strip('\n\n')
                ReadLines.append(line)

    # the regressive step checker
    line1 = ReadLines[-1]
    par1 = ReadMCMCline(line1,ParNames)
    frac = par1['frac']
    istep = par1['istep']+1
    acr = par1['acr']
    diff_check = 0
    iLine = 0
    
    while abs(diff_check) <= 1e-32:
        line0 = ReadLines[-1-iLine]
        par0 = ReadMCMCline(line0,ParNames)
        for key in ModelPars.keys():
            if ModelPars[key]['open']:
                diff_check += par0[key]-par1[key]
        iLine += 1
    print >> OutFileContinueStep, ' Continue @ istep = ', istep

    OutFile.close()
    OutFileContinueStep.close()
    os.system('mv -v %s %s' % (CopyFile,file))
    newModelPars = MakeModelParsContinue(par0,par1,ModelPars)
    return newModelPars, istep, frac, acr

def ReadMCMCheader(OutFile):
    """ Read the first commented line of an MCMC header file. """

    File = open(OutFile,'r')
    File = File.readlines()

    for line in File:
        if line.startswith('#'):
            line = line.strip('#').strip('|:\n\n')
            tags = map(str,line.split('|'))
            param_tagorder = {}
            headerline = line
            for el in range(len(tags)-5):
                if tags[el].strip() != 'istep' or tags[el].strip() != 'acr' or \
                tags[el].strip() != 'chi1' or tags[el].strip() != 'chi2' or \
                tags[el].strip() != 'frac':
                    param_tagorder[el] = tags[el].strip()

    return param_tagorder

def PrintModelParams(ModelParams,OutFile):
    """ Given the dictionary of Model parameters, this routine write a file in the format of the 
        starting parameter files
    """

    OutFileObject = open(OutFile,'w')

    print >> OutFileObject, '# Parname | value | step | open | printformat '
    for param in ModelParams.keys():
        if param == 'RefFilt':
            print >> OutFileObject, param+'  |  '+str(ModelParams[param]['value'])+' | '\
            +str(ModelParams[param]['step'])+' | '\
            +str(ModelParams[param]['open'])+' | '+str(ModelParams[param]['printformat'])
        else:
            print >> OutFileObject, param+'  |  '+str(format(ModelParams[param]['value'],ModelParams[param]['printformat']))+' | '\
            +str(format(ModelParams[param]['step'],ModelParams[param]['printformat']))+' | '\
            +str(ModelParams[param]['open'])+' | '+str(ModelParams[param]['printformat'])

    OutFileObject.close()
    return

def ReadBoundFile(file):
    """ Reads the bounds parameter file and returns the BoundParam dictionary"""

    fileObject = open(file,'r')
    fileObjectLines = fileObject.readlines()
    BoundParams = {}
    for line in fileObjectLines:
        if not line.startswith('#'):
            dummy_array = map(str,line.split('|'))
            BoundParams[dummy_array[0].strip()] =\
            {'open':String2Bool(dummy_array[1].strip())}

    return BoundParams