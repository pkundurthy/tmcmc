
import os
import sys
import cPickle as pickle
import tmcmc
import numpy as np
import class_fitprep as cfp

MainPath = cfp.MainPath
DataPrepPath = MainPath+'DataPrep/'

detrendPars = ['airmass','x1','y1','x2','y2','a0','sky_ratio1','sky_ratio2',\
               'gsky','msky1','msky2','diff_sky','sD1','sD2','sF1','sF2','telrot','telfocus','dist',\
               'index']
           
dataPars = ['flux_ratio']

detrendHeader = '#airmass| x1 | y1 | x2 | y2 | a0 | sky_ratio1 | sky_ratio2 |'
detrendHeader += 'gsky|msky1|msky2|diff_sky|sD1|sD2|sF1|sF2|telrot|telfocus|dist|index'
LCHeader = '# BJD | flux_ratio | errors'


def mkObsDataLine(ObservedData,index_i):
    """
    """
    
    obsdata = ObservedData['x'][index_i]+' | '+ObservedData['y'][index_i]+' | '+ObservedData['yerr'][index_i]
    return obsdata
    
def mkNusDataLine(NuisanceData,index_i):
    """
    """

    nusLine = ''
    for i in detrendPars:
        nusLine += NuisanceData['dtparams'][detrendPars[i]]['data'][index_i]

    return nusLine


def LClineFromIndex(outdict,index_i):
    """
        
    """

    line = ''
    for key in ['time','flux_ratio','err_fluxratio']:
        line = str(outdict['time'][index_i])+'|'\
               +str(outdict['flux_ratio'][index_i])+'|'\
               +str(outdict['err_fluxratio'][index_i])

    return line

def dtlineFromIndex(outdict,index_i):
    """
    
    """
    
    line = ''
    for i in range(len(detrendPars)):
        if i == 0:
            line += str(outdict[detrendPars[i]][index_i])
        else:
            line += '|'+str(outdict[detrendPars[i]][index_i])
    
    return line
    

def getTT(fileName,ObjectName):
    """
        return transit tag from ObjectName_YYYY(MON)DD(s).APXX.data
    """
    
    NameSplit = map(str, fileName.split('.'))
    SplitMore = map(str, NameSplit[0].split('_'))

    Date = SplitMore[1].strip('s')
    for key in cfp.DateStrings[ObjectName].keys():
        #print Date, cfp.DateStrings[ObjectName][key]
        if cfp.DateStrings[ObjectName][key] == Date:
            return key

def getAP(fileName):
    """
        return transit tag
    """
    
    NameSplit = map(str, fileName.split('.'))
    APNUM = NameSplit[1].strip('AP')
    return APNUM

def writeUpdatedNuisance(FileName, dt_data):
    """         """

    FileObject = open(FileName,'w')
    print >> FileObject, detrendHeader

    NData = len(dt_data['index'])
    
    for iLen in range(NData):
        dtline = ''
        for iPar in range(len(detrendPars)):
            keyName = detrendPars[iPar]
            #print keyName, len(dt_data[keyName])
            #print dt_data
            if iPar == 0:
                dtline += str(dt_data[keyName][iLen])
            else:
                dtline += '|'+str(dt_data[keyName][iLen])

        #print dtline
        print >> FileObject, dtline
            
    FileObject.close()
    

def readNusFile(FileName):
    """         """
    
    FileObject = open(FileName,'r')
    FileObject = FileObject.readlines()
    
    Data_Dict = {}
    keyList = [] 
    for line in FileObject:
        if line.startswith('#'):
            dsplit = map(str, line.strip('#').split('|'))
            keyList = []
            for i in range(len(dsplit)):
                exec "%s = [] " % dsplit[i].strip()
                #print "%s = [] " % dsplit[i].strip()
                keyList.append(dsplit[i].strip())
        else:
            dsplit = map(float, line.strip('#').split('|'))
            for i in range(len(dsplit)):
                exec "%s.append(%s)" % (keyList[i],str(dsplit[i]))
                #print "%s.append(%s)" % (keyList[i],str(dsplit[i]))
                 
    for key in keyList:
        exec "Data_Dict[\'%s\'] = np.array(%s) " % (key, key)
        #print "Data_Dict[\'%s\'] = np.array(%s) " % (key, key)
        
    return Data_Dict

def readDataFile(DataFile):
    """    """
    
    DataDictionary, Header = tmcmc.iobinning.ReadData(DataFile)
    Nlen = len(DataDictionary['(BJD)']) 
    outdata = {'time':[],'flux_ratio':[],'err_fluxratio':[],'index':[],\
               'dist':[],'diff_sky':[],'sky_ratio1':[],'sky_ratio2':[],\
               'telfocus':[],'telrot':[]}

    for i in range(Nlen):
        try:
            err = (1e0/DataDictionary['f2'][i])*\
            np.sqrt(DataDictionary['erf1sq'][i] + DataDictionary['erf2sq'][i]*\
            (DataDictionary['f1'][i]/DataDictionary['f2'][i])**2)
        except:
            err = float('inf')

        if DataDictionary['f1'][i] == 0.0 or DataDictionary['f2'][i] == 0.0 or \
        DataDictionary['f1'][i] < 0.0 or DataDictionary['f2'][i] < 0.0 or err > 0.05:
            # add error rejection and large sky rejection here
            pass
        else:
            # compute flux ratios
            outdata['flux_ratio'].append(DataDictionary['f1'][i]/DataDictionary['f2'][i])
            outdata['err_fluxratio'].append(err)
            outdata['time'].append(DataDictionary['JDprefix']+DataDictionary['(BJD)'][i])
            outdata['index'].append(i)
    
            dist = np.sqrt((DataDictionary['x1'][i]-DataDictionary['x2'][i])**2 \
            + (DataDictionary['y1'][i]-DataDictionary['y2'][i])**2)
            diff_sky = DataDictionary['msky1'][i]-DataDictionary['msky2'][i]
            sky_ratio1 = DataDictionary['msky1'][i]/DataDictionary['gsky'][i]
            sky_ratio2 = DataDictionary['msky2'][i]/DataDictionary['gsky'][i]

            outdata['dist'].append(dist)
            outdata['diff_sky'].append(diff_sky)
            outdata['sky_ratio1'].append(sky_ratio1)
            outdata['sky_ratio2'].append(sky_ratio2)
            outdata['telfocus'].append(0e0)
            outdata['telrot'].append(0e0)
    
    for key in DataDictionary.keys():
        if key != '(BJD)' and key != 'f1'  and key != 'f2' and key != 'erf1sq' \
        and key != 'erf2sq' and key != 'ootfg' and key != 'JDprefix' and key != 'time':
            outdata[key] = DataDictionary[key]
            
    return outdata

def ToBeBinned(ObjectName,TT):
    """          """
    
    Out = False
    if ObjectName == 'WASP2' and float(TT.strip('T')) < 8:
        Out = True
        
    if ObjectName == 'XO2' and float(TT.strip('T')) < 5:
        Out = True
    
    return Out

def getOpenNusPars(NuisanceData,TT):
    """         """
    
    OpenList = []
    for dtpar in NuisanceData[TT]['dtparams'].keys():
        if NuisanceData[TT]['dtparams'][dtpar]['used']:
            OpenList.append(dtpar)

    return OpenList

def mkNuisance(NuisanceData):
    """         """
    
    NewNuisance = {}
    NoneKeyList = []
    lenD = {}
    for TT in NuisanceData.keys():
        if TT.startswith('T'):
            NewNuisance[TT] = {}
            for key in NuisanceData[TT]['dtparams'].keys():
                if NuisanceData[TT]['dtparams'][key]['used']:
                    NewNuisance[TT][key] = NuisanceData[TT]['dtparams'][key]['data']
                    lenD[TT] = len(NuisanceData[TT]['dtparams'][key]['data'])
                else:
                    NoneKeyList.append( (TT,key) )

    for el in NoneKeyList:
        TT = el[0]
        key = el[1]
        try:
            NewNuisance[TT][key] = np.zeros(lenD[TT])
        except:
            NewNuisance[TT][key] = np.zeros(0)

    return NewNuisance
    
def applyGoodIDs(ObservedData,NuisanceData,goodids):
    """                         """
    
    outdata = {}
    x = np.array(ObservedData['x'])
    y = np.array(ObservedData['y'])
    yerr = np.array(ObservedData['yerr'])
    
    outdata['time'] = x[goodids]
    outdata['flux_ratio'] = y[goodids]
    outdata['err_fluxratio'] = yerr[goodids]
    
    for par in detrendPars:
        d = np.array(NuisanceData[par])
        outdata[par] = d[goodids]

    return outdata

def BinnedData(outdata,binsize):
    """                          """
    
    bins = binsize/86400e0
    BinnedData = {}
    
    for key in detrendPars:
        if len(outdata['time']) > 0:
            x = outdata['time']
            ydt = outdata[key]
            yerr_dt = np.zeros(len(x))
            bin_x, bin_y, bin_prop_err, bin_err, bin_points = \
            tmcmc.binning.GridBinning(x,ydt,yerr_dt,bins)
            BinnedData[key] = bin_y
        else:
            BinnedData[key] = []

    if len(outdata['time']) > 0:
        x = outdata['time']
        ydt = outdata['flux_ratio']
        yerr_dt = outdata['err_fluxratio']
        bin_x, bin_y, bin_prop_err, bin_err, bin_points = tmcmc.binning.GridBinning(x,ydt,yerr_dt,bins)
        BinnedData['time'] = bin_x
        BinnedData['flux_ratio'] = bin_y
        BinnedData['err_fluxratio'] = bin_err
    else:
        BinnedData['time'] = []
        BinnedData['flux_ratio'] = []
        BinnedData['err_fluxratio'] = []
        
    return BinnedData
    
def normalizeFluxRatio(outdata,T0,tT,tG):
    """   """
    
    T1 = T0 - (tT/2e0) - (tG/2e0)
    T4 = T0 + (tT/2e0) + (tG/2e0)
    #T2 = T1 + tG
    #T3 = T4 - tG
    IngressTime = T1
    EgressTime = T4

    flat_flux = []
    for i in range(len(outdata['time'])):
        if outdata['time'][i] < IngressTime or outdata['time'][i] > EgressTime:
            flat_flux.append(outdata['flux_ratio'][i])

    normalizing_factor = np.median(np.array(flat_flux))
    if np.isnan(normalizing_factor):
        normalizing_factor = 1e0

    outdata['flux_ratio'] = np.array(outdata['flux_ratio'])/normalizing_factor
    
    return outdata, normalizing_factor
    
def writeLCFile(ObservedData,outfile):
    """         """
    
    FileObj = open(outfile, 'w')
    
    print >> FileObj,LCHeader
    for i in range(len(ObservedData['x'])):
        timeStr = format(ObservedData['x'][i],'.7f')
        flux_str = format(ObservedData['y'][i],'.12f') 
        flux_err = format(ObservedData['yerr'][i],'.12f') 
        print >> FileObj, timeStr+'|'+flux_str+'|'+flux_err

    FileObj.close()

def SecondRejectOutliers(DetrendedData,ModelData,sigma,TT):
    """                                     """
    
    scatter1 = np.abs(np.array(DetrendedData['y'])-np.array(ModelData['y']))
    mm1, sdv1, ngood1, goodindex1, badindex1 = tmcmc.binning.MedianMeanOutlierRejection(scatter1,sigma,'median')
    scatter2 = DetrendedData['yerr']
    mm2, sdv2, ngood2, goodindex2, bad_err = tmcmc.binning.MedianMeanOutlierRejection(scatter2,3e0,'median')
    #bad_err = np.where(scatter2 > 0.01e0)[0]
    
    DetrendedData['y'][bad_err] = float('inf')
    scatter = np.abs(np.array(DetrendedData['y'])-np.array(ModelData['y']))
    #print len(scatter), sigma, baderr, TT
    mm, sdv, ngood, goodindex, badindex = \
    tmcmc.binning.MedianMeanOutlierRejection(scatter,sigma,'median')
    goodi = goodindex
    badi = badindex

    return goodi, badi, bad_err

def rejectOutliers(DetrendedData,ModelData,sigmas):
    
    goodi = {}
    badi = {}
    for TT in DetrendedData.keys():
        if TT.startswith('T'):
            scatter = np.abs(np.array(DetrendedData[TT]['y'])-np.array(ModelData[TT]['y']))
            mm, sdv, ngood, goodindex, badindex = tmcmc.binning.MedianMeanOutlierRejection(scatter,sigmas,'median')
            goodi[TT] = goodindex
            badi[TT] = badindex
    
    return goodi, badi

def SwitchOFF(NuisanceData,OffList,TTagList):
    """                      """

    for TT in TTagList:
        for dtpars in OffList:
            NuisanceData[TT]['dtparams'][dtpars]['used'] = False

    OnList = []
    for dtpar in NuisanceData[TT]['dtparams'].keys():
        if not dtpar in OffList:
            NuisanceData[TT]['dtparams'][dtpar]['used'] = True
            OnList.append(dtpar)

    return NuisanceData, OnList

def getSwitchLine(ObjectName,TT,**kwargs):
    
    passNus = False
    for key in kwargs:
        if key.lower() == 'supress':
            passNus = kwargs[key]

    NuisanceTags = {}
    OpenList = detrendPars
    for i in range(len(detrendPars)):
        NuisanceTags[detrendPars[i]] = True

    TTnum = float(TT.strip('T'))
    if not passNus:
        if ObjectName == 'WASP2':
            if TTnum == [1]:
                OpenList = ['gsky','dist','diff_sky','airmass','x1','y1','sF1','sD1']
            if TTnum == [2]:
                OpenList = ['airmass','dist','sky_ratio1','diff_sky','x1','y1','sF1','sD1']
            if TTnum in [3,4,5,6,7]:
                OpenList = ['airmass','dist','a0','diff_sky','x1','y1','sF1','sD1']
            if TTnum in [8,9,10]:
                OpenList = ['airmass','dist','diff_sky','gsky','index','x1','y1','sF1','sD1']

            for parDT in NuisanceTags.keys():
                    if not parDT in OpenList:
                        NuisanceTags[parDT] = False

        if ObjectName == 'XO2':
            if TTnum == [1,2,3]:
                OpenList = ['gsky','dist','diff_sky','airmass','x1','y1','sF1','sD1']
            if TTnum == [4]:
                OpenList = ['airmass','dist','sky_ratio1','diff_sky','a0','x1','y1','sF1','sD1']
            if TTnum in [5,6,7]:
                OpenList = ['airmass','dist','a0','diff_sky','x1','y1','sF1','sD1']
            if TTnum in [7,8,9,10]:
                OpenList = ['airmass','dist','diff_sky','gsky','x1','y1','sF1','sD1']

            for parDT in NuisanceTags.keys():
                    if not parDT in OpenList:
                        NuisanceTags[parDT] = False
            
        if ObjectName == 'TRES3':
            NuisanceTags['a0'] = False
            NuisanceTags['sD2'] = False
            NuisanceTags['sF2'] = False
            NuisanceTags['x2'] = False
            NuisanceTags['y2'] = False
            NuisanceTags['sky_ratio2'] = False
            NuisanceTags['msky2'] = False
            NuisanceTags['msky1'] = False
            NuisanceTags['telrot'] = False
            NuisanceTags['index'] = False
            #NuisanceTags['dist'] = False
            #NuisanceTags['diff_sky'] = False
            #if TTnum == 9:
                #NuisanceTags['sD1'] = False
                ##NuisanceTags['dist'] = True
                #NuisanceTags['sF2'] = True
    else:
        if ObjectName == 'WASP2':
            NuisanceTags['telfocus'] = False
            NuisanceTags['telrot'] = False
            NuisanceTags['index'] = False
            if TTnum > 7:
                NuisanceTags['a0'] = False
        if ObjectName == 'XO2':
            NuisanceTags['telfocus'] = False
            NuisanceTags['telrot'] = False
            NuisanceTags['index'] = False
            if TTnum > 6:
                NuisanceTags['a0'] = False

    switchline = ''
    for i in range(len(detrendPars)):
        if NuisanceTags[detrendPars[i]]:
            switchline += '| 1 '
        else:
            switchline += '| 0 '
            
    return switchline

def chisq(Data,ModelData):
    
    #yobs = np.array([])
    #yerr = np.array([])
    #ymod = np.array([])
    yobs = []
    ymod = []
    yerr = []
    for i in range(len(Data['all']['tagorder'])):
        Tag = Data['all']['tagorder'][i+1]
        yobs.extend(Data[Tag]['y'])
        yerr.extend(Data[Tag]['yerr'])
        ymod.extend(ModelData[Tag]['y'])

    DataOut = Data.copy()
    #print Data['T1']['x']
    DataOut['all']['yerr'] = yerr
    #yobs = Data['all']['y']
    #yerr = Data['all']['yerr']
    #ymod = ModelData['all']['y']
    return tmcmc.mcmc.chisq(yobs,yerr,ymod), DataOut

def NOpen(ModelParams):
    
    NOpen = 0
    for par in ModelParams.keys():
        if ModelParams[par]['open']:
            NOpen += 1

    return NOpen

def NTTs(ModelParams):
    
    NTTs = 0
    for par in ModelParams.keys():
        if par.startswith('T0'):
            if ModelParams[par]['open']:
                NTTs += 1

    return NTTs

def HiRes(ObservedData,Num):

    HiRes = {}
    allTimes =  np.array([])
    for TT in ObservedData.keys():
        if TT.startswith('T'):
            if len(ObservedData[TT]['x']) > 0:
                x = np.linspace(min(ObservedData[TT]['x']),max(ObservedData[TT]['x']),Num)
                #print min(x), max(x)
                allTime = np.hstack( (allTimes,x) )
                HiRes[TT] = {'x':x}
            else:
                x = np.array([])
                HiRes[TT] = {'x':x}
                allTime = np.hstack( (allTimes,x) )
    
    HiRes['all']= {'x':allTime,'tagorder':ObservedData['all']['tagorder']}
    
    return HiRes

def get_optap(rms,TT):
    """                """
    
    ap_list = []
    rms_list = []
    
    for AP in rms.keys():
        ap_list.append(float(AP))
        rms_list.append(rms[AP][TT])
        
    return np.array(ap_list), np.array(rms_list)