

def ReadSingleTAP_DataFile(fileName):
    """ Returns a dictionary pf x,y,yerr data after reading a generic data file.
        Data file should have the following form:
        col 1 = x (abscissa) , col 2 = y (ordinate)  , col 3 = yerr (error in ordinate)
        Lines starting with '#' are treated as comments and skipped.
    """
    
    file_object = open(fileName,'r')
    file_object = file_object.readlines()
    data_point_count = 0
    
    # Empty arrays for data
    x=[]
    y = []
    yerr = []
    data_out = {}

    for line in file_object:
        if not line.startswith('#'):
            dummy_array = map(str,line.split())
            data_point_count += 1
            x.append(float(dummy_array[0]))
            y.append(float(dummy_array[1]))
            yerr.append(float(dummy_array[2]))

    data_out['all'] = {'x':x,'y':y,'yerr':yerr}
    # print str(data_point_count)+' data points read'
    return data_out

def print_TAPerr(InputFile,OutputFile):
    
    PrintReady = readTAPMCMC_SplitSections(InputFile)
    header = '# parname     |    value   | lower   | upper    | useSingle ?'
    OFileObject = open(OutputFile,'w')
    print header
    print >> OFileObject, header
    for par in PrintReady:
        value = PrintReady[par]['value']
        lower = PrintReady[par]['lower']
        upper = PrintReady[par]['upper']
        useSingle = PrintReady[par]['useSingle']
        outLine = par+' | '+value+' | '+lower+' | '+upper+' | '+str(useSingle)
        print outLine
        print >> OFileObject, outLine


def readTAPMCMC_SplitSections(filename):
    """ Extract Info from table  """
    
    TableFile = open(filename,'r')
    TableFile = TableFile.readlines()
    
    NLines = len(TableFile)
    ParTable = 0
    LinkTable = 0
    
    EndString_1 = '\\label{tbl:mcmcpar}'
    EndString_2 = '\\label{tbl:tapmcmc1}'
    EndString_3 = 'locked together in the MCMC analysis.}\n'
   
    ParSec = {}
    LinkSec = {}
    StartID = 0
    EndID = NLines-1
    Switch = ''
    for iLine in range(NLines):
        line = TableFile[iLine]

        #switch to tell if reading transit list
        if line.startswith('\\tablecaption{Overview'):
            Switch = 'TT'
            StartID = iLine
            #print 'TTags Start', iLine
        if line.startswith(EndString_1):
            EndID = iLine
            #print 'TTags End', iLine
        if Switch == 'TT': TTSection = TableFile[StartID:EndID]
        
        #switch to tell if reading parameter estimates
        if line.startswith('\\tablecaption{Wavelet'):
            Switch = 'Par'
            StartID = iLine
            ParTable += 1
            #print 'MCMC Pars Start', iLine, ParTable
        if line.startswith(EndString_2):
            EndID = iLine
            #print 'MCMC Pars End', iLine, ParTable
        if Switch == 'Par': ParSec[ParTable] = TableFile[StartID:EndID]
        
        #switch to tell if reading parameter links
        if line.endswith('{MCMC Parameter Set} \\\\\n'):
            Switch = 'Link'
            StartID = iLine
            LinkTable += 1
            #print 'Link Pars Start', iLine, LinkTable
        if line.endswith(EndString_3):
            EndID = iLine
            #print 'Link Pars End', iLine, LinkTable
        if Switch == 'Link': LinkSec[LinkTable] = TableFile[StartID:EndID]

    TTList = TTSort(TTSection)
    ColLinkSort = ColTTSort(LinkSec)
    ColParSort = ColTTSort(ParSec)
    
    LinkData = GetData(LinkSec,ColLinkSort,TTList)
    ParData = GetData(ParSec,ColParSort,TTList)
    
    FinalParDict = SortData(LinkData,ParData)

    return FinalParDict
        
def FilterCheck(LinkData):
    
    TTList = LinkData.keys()
    TT0 = TTList[0]
    ParList = LinkData[TT0].keys()
    
    FiltList = []
    for par in ParList:
        for TT in TTList:
            ValueStrip = LinkData[TT][par]['value'].strip()
            if par == 'RpRs':
                FiltList.append(ValueStrip)

    UniqueFilter = list(set(FiltList))
    FiltDict = {}
    for filt in UniqueFilter:
        FiltDict[filt] = []

    for par in ParList:
        for TT in TTList:
            ValueStrip = LinkData[TT][par]['value'].strip()
            if par == 'RpRs': 
                FiltDict[ValueStrip].append(long(TT.strip('T')))
    
    FilterMatch = {}
    for filt in FiltDict.keys():
        FilterTag = ''
        for el in sorted(list(set(FiltDict[filt]))):
             FilterTag += '.T'+str(el)
        FilterMatch[filt] = FilterTag

    return FilterMatch

def SortData(LinkData,ParData):
    """             """
    
    ParOut = {}
    TTList = LinkData.keys()
    TT0 = TTList[0]
    ParList = LinkData[TT0].keys()
    
    FiltMatch = FilterCheck(LinkData)
    
    for par in ParList:
        for TT in TTList:
            ValueStrip = LinkData[TT][par]['value'].strip()
            if ValueStrip == TT.strip('T'):
                if par == 'T0' or par == 'sigwhite' or par == 'sigred':
                    newPar = par+'.'+TT
                    ParOut[newPar] = ParData[TT][par]
                elif par == 'RpRs' or par == 'u1' or par == 'u2':
                    newPar = par+FiltMatch[ValueStrip]
                    ParOut[newPar] = ParData[TT][par]
                else:
                    newPar = par
                    ParOut[newPar] = ParData[TT][par]
            else:
                pass

    return ParOut

def parStringConvert(parName):
    
    parString = ''
    if parName == 'Airmass Y-int':
        parString = 'A0'
    if parName == 'Airmass Slope':
        parString = 'A1'
    if parName == 'Sigma Red':
        parString = 'sigred'
    if parName == 'Sigma White':
        parString = 'sigwhite'
    if parName == 'Period':
        parString = parName
    if parName == 'Inclination':
        parString = 'inc'
    if parName == 'a/R*':
        parString = 'aRs'
    if parName == 'Rp/R*':
        parString = 'RpRs'
    if parName == 'Mid Transit':
        parString = 'T0'
    if parName == 'Linear LD':
        parString = 'u1'
    if parName == 'Quad LD':
        parString = 'u2'
    if parName == 'Eccentricity':
        parString = 'ecc'
    if parName == 'Omega':
        parString = 'omega'

    return parString
    
def Line2Data(line,ColSort,key,DataParDict):
    """         """
    
    SplitLine = map(str, line.split('&'))
    parName = SplitLine[0].strip()
    for iEntry in range(len(SplitLine)-1):
        Entry = SplitLine[iEntry+1]
        NewEntry = Entry.replace('$^{+','|').replace('}_{-','|').replace('}$','')
        SplitEntry = map(str, NewEntry.split('|'))
        #print SplitEntry
        if len(SplitEntry) > 1:
            value = SplitEntry[0]
            upper = SplitEntry[1]
            lower = SplitEntry[2]
            useSingle = False
        else:
            value = NewEntry.replace('\\tablenotemark{a}','')
            upper = 'nan'
            lower = 'nan'
            useSingle = False

        if float(upper) == float(lower):
            useSingle == True

        parString = parStringConvert(parName)

        TT = ColSort[key][iEntry+1]
        DataParDict[TT][parString] = {'value':value,'lower':lower,'upper':upper,'useSingle':useSingle}

    return DataParDict

def GetData(Section,ColSection,TTList):
    """             """
    
    DataParDict = {}
    for TT in TTList:
        DataParDict[TT] = {}

    for key in Section.keys():
        #print key, ColSection[key]
        for line in Section[key]:
            if line.endswith('\\\\\n') and not line.startswith('& \\multicolumn{'):
                line_in = line.strip('\\\\\n').strip()
                DataParDict = Line2Data(line_in,ColSection,key,DataParDict)
    
    return DataParDict

def ColTTSort(Section):
    """             """
    
    SplitTableDict = {}
    for key in Section.keys():
        ColNum = 0
        SplitTableDict[key] = {}
        for line in Section[key]:
            if line.strip().startswith('& \\colhead{'):
                ColNum += 1
                SplitTableDict[key][ColNum] = getcolTTag(line.strip())

    return SplitTableDict

def TTSort(Section):
    """             """
    
    TTList = []
    for line in Section:
        if line.startswith('Transit'):
            TTList.append(getTTag(line))
            
    return TTList

def getcolTTag(line):
    """ get transit tag """
    
    LineSplit = map(str, line.split(':'))
    TTag = 'T'+str(long(LineSplit[0].strip('& \{colhead ')))
    
    return TTag

def getTTag(line):
    """ get transit tag """
    
    LineSplit = map(str, line.split('&'))
    TTag = 'T'+str(long(LineSplit[0].strip('Transit ')))
    
    return TTag

def getTAP_TTs(Section):
    
    ErrDict = {}
    for sec in Section.keys():
        for line in Section[sec]:
            if line.startswith('\\tablecaption'):
                pass
        
        if 'Overview of TAP MCMC Parameters' in Section[sec]:
            pass
