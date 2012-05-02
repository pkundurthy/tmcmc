
import os
import sys
import tmcmc
import random
import numpy as np
import cPickle as cP
import itertools
from tmcmc.workingfolder_setup import get_user_exec

ExecList = get_user_exec()
for Ex in ExecList:
    exec(Ex)

#FitType
DateStrings =  cP.load(open(PicklePath+'DateInfo.pickle','rb'))
DatePrintStrings =  cP.load(open(PicklePath+'DateString.pickle','rb'))
ParDict = cP.load(open(PicklePath+'MCMC_MINUIT_StartInfo.pickle','rb'))
ExpectedTT = cP.load(open(PicklePath+'ExpectedTT.pickle','rb'))
#FirstOptAp = cP.load(open(PicklePath+'OptApGuess.pickle','rb'))
BoundPars = cP.load(open(PicklePath+'BoundPar.pickle','rb'))
FuncName = 'MTQ_multidepth_tduration'

CaseList = ['MCMC.FLD','MCMC.OLD','MCMC.MDFLD',\
            'MINUIT.FLD','MINUIT.OLD','MINUIT.MDFLD','MINUIT.FIRSTTRY']

def sortTTdata(TTDicts,fitList,PeriodGuess):
    """             """

    allTT = np.array([])
    allErrTT = np.array([])
    
    for fitName in fitList:
        #print fitName, len(TTDicts[fitName][0]), TTDicts[fitName][0]
        allTT = np.hstack((allTT,TTDicts[fitName][0]))
        allErrTT = np.hstack((allErrTT,TTDicts[fitName][1]))

    minTT = min(allTT)
    epoch_raw = (allTT - minTT)/PeriodGuess
    epoch_all = np.around(epoch_raw)
    OutFitDict = {}
    for fitName in fitList:
        epochr = (TTDicts[fitName][0] - minTT)/PeriodGuess
        epocha = np.around(epochr)
        OutFitDict[fitName] = {'epoch':epocha,\
                               'TT':TTDicts[fitName][0],\
                               'errTT':TTDicts[fitName][1]}

    return epoch_all, allTT, allErrTT, OutFitDict

def getParDict(ObjectName):
    
    ParFiles = {}
    Obj = Object(ObjectName)

    Obj.InitiateCase('MCMC.FLD')
    for fitNum in [1,2]:
        Obj.InitiateFitNum(fitNum)
        ParFiles['MCMC.FLD.'+str(fitNum)] = Obj.ParErrorFile

    Obj.InitiateCase('MCMC.OLD')
    for fitNum in [1,2]:
        Obj.InitiateFitNum(fitNum)
        ParFiles['MCMC.OLD.'+str(fitNum)] = Obj.ParErrorFile

    Obj.InitiateCase('MCMC.MDFLD')
    for fitNum in [1,2]:
        Obj.InitiateFitNum(fitNum)
        ParFiles['MCMC.MDFLD.'+str(fitNum)] = Obj.ParErrorFile

    Obj.InitiateCase('MINUIT.FLD')
    for fitNum in [1,2]:
        Obj.InitiateFitNum(fitNum)
        ParFiles['MINUIT.FLD.'+str(fitNum)] = Obj.ParErrorFile

    Obj.InitiateTAP()
    Obj.setTAPErrorFile()
    ParFiles['TAP'] = Obj.ParErrorFile

    for fileName in os.listdir(Obj.objectPath+'LitData/'):
        if fileName.endswith('.err'):
            SplitName = map(str, fileName.split('.'))
            fitName = SplitName[0].strip()
            ParFiles[fitName] = Obj.objectPath+'LitData/'+fileName

    ParDict = {}
    for fitName in ParFiles.keys():
        #print ParFiles[fitName]
        ParDict[fitName] = tmcmc.iopostmcmc.readErrorFile(ParFiles[fitName])

    return ParDict, ParFiles, Obj

def GetPeriodFits(ParDict):
    """             """

    OutDict = {}
    for fitName in ParDict.keys():
        try:
            OutDict[fitName] = (ParDict[fitName]['Period']['value'],\
                           max([ParDict[fitName]['Period']['lower'],\
                                ParDict[fitName]['Period']['upper']]))
        except:
            pass
    
    return OutDict

def GetTTFits(ParDict):
    """             """
    
    OutDict = {}
    for fitName in ParDict.keys():
        TTarr = np.array([])
        errTTarr = np.array([])
        for par in ParDict[fitName].keys():
            if par.startswith('T0.'):
                TTarr = np.hstack( (TTarr,ParDict[fitName][par]['value']))
                err = max([ParDict[fitName][par]['lower'],\
                           ParDict[fitName][par]['upper']])
                errTTarr = np.hstack( (errTTarr,err))

        if len(TTarr) > 0:
            OutDict[fitName] = (TTarr,errTTarr)

    return OutDict

def OpenParArray(ModelParams):
    """         """
    
    OpenList = []
    for parKey in ModelParams.keys():
        if ModelParams[parKey]['open']:
            OpenList.append(parKey)

    return OpenList

def MakeStartParams(ObjectName,FitID):
    """                     """
    
    CommonAll = ['tG','tT','RefFilt','f0']

    StartParams = {}
    for key in CommonAll:
        StartParams[key] = ParDict[ObjectName][key]
        if key == 'RefFilt':
            StartParams[key]['value'] = float('nan')
            if isinstance(StartParams[key]['printformat'],list):
                if FitID.upper() == 'OLD' or FitID.upper() == 'FLD':
                    StartParams[key]['printformat'] = StartParams[key]['printformat'][0]
                else:
                    StartParams[key]['printformat'] = StartParams[key]['printformat'][1]
        
    for key in ParDict[ObjectName].keys():
        if key.startswith('NT.') or key.startswith('T0.'):
            StartParams[key] = ParDict[ObjectName][key]
        
        if FitID.upper() == 'OLD' or FitID.upper() == 'FLD':
            if key.startswith('v') or key.startswith('D'):
                keysplit = map(str, key.split('.'))
                if len(keysplit) > 2:
                    StartParams[key] = ParDict[ObjectName][key]
                    StartParams[key]['open'] = True
                    if key.startswith('v') and FitID.upper() == 'OLD':
                        StartParams[key]['open'] = True
                    if key.startswith('v') and FitID.upper() == 'FLD':
                        StartParams[key]['open'] = False
                        StartParams[key]['step'] = 0.00
        elif FitID.upper() == 'MDFLD':
            if key.startswith('D'):
                keysplit = map(str, key.split('.'))
                if len(keysplit) == 2:
                    StartParams[key] = ParDict[ObjectName][key]
            if key.startswith('v'):
                keysplit = map(str, key.split('.'))
                if len(keysplit) > 2:
                    StartParams[key] = ParDict[ObjectName][key]
                    StartParams[key]['open'] = False
                    StartParams[key]['step'] = 0.00
    
    return StartParams

def ApplyShift(StartParams,fitNum,Shift):
    """             """

    OpenPars = OpenParArray(StartParams)
    LenOpen = len(OpenPars)
    if long(fitNum) == 1:
        ShiftList = np.arange(LenOpen)%2
    elif long(fitNum) == 2:
        ShiftList = (np.arange(LenOpen)+1)%2
    elif long(fitNum) == 3:
        ShiftList = np.zeros(LenOpen)+1
    else:
        raise NameError("fitNum %s not recognized" % str(fitNum))

    for iPar in range(LenOpen):
        Param = OpenPars[iPar]
        if ShiftList[iPar] == 1:
            StartParams[Param]['value'] += Shift*StartParams[Param]['step']
    
    return StartParams

def SwitchClosedAll(ModelParams):
    
    OpenPars = OpenParArray(ModelParams)
    for Param in OpenPars:
        ModelParams[Param]['open'] = False

    return ModelParams

def readTAPdata(Path):
    """             """
    
    DT = {}
    for fileName in os.listdir(Path):
        if fileName.endswith('.lcdtx') and \
           not fileName.endswith('ALL.lcdtx'):
            SplitName = map(str, fileName.split('.'))
            DT[SplitName[1].strip()] = tmcmc.ioTAP.ReadSingleTAP_DataFile(Path+'/'+fileName)

    return DT
        
def getTAPfitTables(casePath):
    """ return path to tex file """
    
    FitDict = {}
    for top, dirs, files in os.walk(casePath):
        if top == casePath:
            Fits = dirs
            for fitDir in Fits:
                for fileName in os.listdir(casePath+'/'+fitDir):
                    if fileName.endswith('tables.tex'):
                        FitDict[fitDir] = casePath+'/'+fitDir+'/'+fileName

    return FitDict

class Object:

    def __init__(self, name):

        self.name = name
        self.ParDict = ParDict[self.name]
        self.TT = ExpectedTT[self.name]
        self.Dates = DatePrintStrings[self.name]
        self.dataPath = MainPath+self.name+'/data/'
        self.objectPath = MainPath+self.name+'/'
        self.lcFileList = self.dataPath+self.name+'.LC.listx' 
        self.nuisONOFF = self.dataPath+self.name+'.NUS.onoffx'

    def InitiateCase(self, CaseID):
        
        self.case = CaseID
        splitCase = map(str, CaseID.split('.'))
        self.fitID = splitCase[1]
        self.fitMethod = splitCase[0].lower()
        self.casePath = MainPath+self.name+'/'+self.case+'/'
        self.FuncName = 'MTQ_multidepth_tduration'
        self.StartParams = MakeStartParams(self.name,self.fitID)
        self.BoundParams = BoundPars[self.FuncName]
        self.BoundFile = self.objectPath+'BOUND.par'
        self.ModelParams = MakeStartParams(self.name,self.fitID)
        self.FuncExecString = "from tmcmc.myfunc import %s as ModelFunc"
        #tmcmc.iomcmc.PrintModelParams(StartParams,self.StartFileName)
        
    def InitiateFitNum(self,fitNum):
        
        self.fitNum = str(fitNum).zfill(4)
        self.StartFile = self.objectPath+'START.'+self.name+'.'+self.fitID+'.'+self.fitNum+'.par'

        FileRoot = self.casePath+self.name+'.'+self.case+'.'+self.fitNum
        self.ErrorFile = FileRoot+self.fitMethod+'.err'
        self.ErrorDerivedFile = FileRoot+self.fitMethod+'.derived.err'
        
        if self.fitMethod.lower() == 'mcmc':

            self.OutFitFile = FileRoot+'.'+self.fitMethod

            self.CroppedFileName = FileRoot+'.crop.'+self.fitMethod

            self.AutoCorStatsFile = FileRoot+'.AutoCorStat'

            self.AutoCorFigRoot = FileRoot+'.AutoCorFit'

            self.TracePlotRoot = FileRoot+'.TracePlot'

            self.CovCorStatsRoot = FileRoot+'.CovCorStat'

            self.LowestChiSQFile = FileRoot+'.lowchisq.par'

            self.ParErrorFile = FileRoot+'.lowchisq.err'

            self.DerivedFile = FileRoot+'.'+self.fitMethod+'.derived.'+self.fitMethod

            self.CroppedDerivedFile = FileRoot+'.'+self.fitMethod+'.derived.crop.'+self.fitMethod

            self.DerivedCovCorStatsRoot = FileRoot+'.derived.CovCorStat'

            self.DerivedLowestChiSQFile = FileRoot+'.lowchisq.derived.par'

            self.DerivedErrorFile = FileRoot+'.lowchisq.derived.err'

            self.DerivedParFile = self.DerivedLowestChiSQFile

            self.OutParFile = self.LowestChiSQFile

        if self.fitMethod.lower() == 'minuit': 

            self.OutParFile = FileRoot+'.'+self.fitMethod+'.par'

            self.OutFitFile = self.OutParFile

            self.ParErrorFile = FileRoot+'.'+self.fitMethod+'.err'

            self.DerivedParFile = FileRoot+'.'+self.fitMethod+'.derived.'+self.fitMethod+'.par'

            self.DerivedErrorFile = FileRoot+'.'+self.fitMethod+'.derived.'+self.fitMethod+'.err'


    def InitiateData(self):

        self.ObservedData = tmcmc.mcmc.ReadMultiList(self.lcFileList)
        self.NuisanceData = tmcmc.mcmc.ReadDetrendFile(self.nuisONOFF)
        exec(self.FuncExecString % self.FuncName)
        self.ModelData = ModelFunc(self.ModelParams,self.ObservedData)
        self.DetrendedData = tmcmc.mcmc.DetrendData(self.ObservedData,self.ModelData,self.NuisanceData,'',False)

    def InitiateTAP(self):
        
        self.case = 'TAP'
        self.fitMethod = 'TAP'
        self.casePath = MainPath+self.name+'/'+self.case+'/'
        self.DetrendedData = readTAPdata(self.casePath)
        self.FitTables = getTAPfitTables(self.casePath)
        
    def printTAP_Output(self):
        
        self.OutFileList = {}
        for fit in self.FitTables.keys():
            self.OutFileList[fit] = self.casePath+'TAP_'+fit+'.err'
            tmcmc.ioTAP.print_TAPerr(self.FitTables[fit],self.OutFileList[fit])

    def setTAPErrorFile(self):
        
        for fit in self.FitTables.keys():
            self.ParErrorFile = self.casePath+'TAP_'+fit+'.err'

    def OtherFitFiles(self,Case):

        self.case = Case
        self.casePath = MainPath+self.name+'/LitData/'
        for fileName in os.listdir(self.casePath):
            #print fileName, Case.lower(), fileName.startswith(Case.lower()), fileName.endswith('.err')
            if fileName.startswith(Case.lower()) and fileName.endswith('.err'):
                self.ParErrorFile = self.casePath+fileName
                #print self.ParErrorFile

    def MakeBoundFile(self):
        """         """

        OutFile = open(self.BoundFile,'w')
        print >> OutFile, '# Bound Func  |  Flag '
        for key in self.BoundParams.keys():
            print >> OutFile, key,' | ',self.BoundParams[key]['open']
        OutFile.close()
        
    def MakeStartFile(self, Shift):
        """         """
        print self.ModelParams
        StartParams = self.ModelParams
        #Bound0 = tmcmc.mcmc.ApplyBounds(self.ModelParams,self.BoundParams)
        Bound = False
        Trial = 1
        while not Bound:
            if Trial%15 == 0:
                Shift /= 2e0
            StartParams = ApplyShift(self.ModelParams,self.fitNum,Shift)
            Bound = tmcmc.mcmc.ApplyBounds(StartParams,self.BoundParams)
            Trial += 1

        tmcmc.iomcmc.PrintModelParams(StartParams,self.StartFile)

    def StepSizeFromExplore(self, FileList, StablePerc):
        """         """

        step = {}
        for fileName in FileList:
            data = tmcmc.iopostmcmc.readMCMC(fileName)
            if data['acr'][-1] > 0.44-StablePerc \
                and data['acr'][-1] < 0.44+StablePerc:
                for par in data.keys():
                    if not tmcmc.iopostmcmc.isNonParam(par):
                        medfrac = np.median(data['frac'][-1000:])
                        print par+' has stabilized, acr = '+format(data['acr'][-1],'.2f')+\
                              ' frac = '+str(medfrac)+' | '+self.name+', '+self.case
                        step[par] = {'frac':medfrac}
            else:
                for par in data.keys():
                    if not tmcmc.iopostmcmc.isNonParam(par):
                        print par+' has NOT stabilized, acr = '+format(data['acr'][-1],'.2f')+\
                              ' | '+self.name+', '+self.case

        for par in step.keys():
            for key in self.ModelParams.keys():
                if key == par:
                    self.ModelParams[par]['step'] = self.ModelParams[par]['step']*step[par]['frac']
                    self.ModelParams[par]['open'] = True

    def UpdateModelParams(self):

        self.ModelParams = tmcmc.iomcmc.ReadStartParams(self.OutParFile)

    def HiResModelLC(self, **kwargs):

        Num = 5e3 # number of points
        DeltaT = 0.2 # days before and after T0 to compute lightcurve
        ModPar = self.ModelParams

        for key in kwargs:
            if key.lower() == 'npoints':
                Num = kwargs[key]
            if key.lower() == 'dt':
                DeltaT = kwargs[key]
            if key.lower() == 'modelpars':
                ModPar = kwargs[key]

        TempObserved = {}
        for par in self.ModelParams.keys():
            if par.startswith('T0.'):
                TT = map(str, par.split('.'))
                TStart = self.ModelParams[par]['value'] - DeltaT
                TEnd = self.ModelParams[par]['value'] + DeltaT
                TempObserved[TT[1].strip()] = {'x':np.linspace(TStart,TEnd,Num)}

        allT = []
        for Tnum in self.ObservedData['all']['tagorder'].keys():
            allT.extend(TempObserved['T'+str(Tnum)]['x']) 

        TempObserved['all'] = {'x':np.array(allT),'tagorder':self.ObservedData['all']['tagorder']}

        exec(self.FuncExecString % self.FuncName)
        HRData = ModelFunc(ModPar,TempObserved)
        for TT in self.ObservedData.keys():
            if TT.startswith('T'):
                HRData[TT]['x'] = TempObserved[TT]['x']

        self.HiResModelData = HRData

    def printDetrendedData(self):
        """             """

        self.DetrendedDataPath = MainPath+self.name+'/TAP/'
        
        TTcount = 0
        for TT in self.DetrendedData.keys():
            if TT.startswith('T'):
                TTcount += 1
        
        FileAllStacked = self.DetrendedDataPath+self.name+'.ALL.lcdtx'
        ALLOutFile = open(FileAllStacked,'w')
        NCount = None
        for TTnum in xrange(TTcount):
            TT = 'T'+str(TTnum+1)
            #if TTnum != TTcount-1: 
                #NCount = self.ModelParams['NT.T'+str(TTnum+2)]['value'] -\
                         #self.ModelParams['NT.'+TT]['value']
                #NCount = long(NCount)
                #if self.name == 'XO2': 
                    #P = 2.615859997
                    #T0 = self.ModelParams['T0.T1']['value']
                #if self.name == 'TRES3': 
                    #P = 1.306187245
                    #T0 = self.ModelParams['T0.T1']['value']
            #else:
                #NCount = None
            #print NCount
            FileName = self.DetrendedDataPath+self.name+'.'+TT+'.lcdtx'
            LCOutFile = open(FileName,'w')
            #print 'writing '+FileName
            #print >> LCOutFile, '# BJD   |   flux   |   err_flux '
            #epoch = self.ModelParams['NT.'+TT]['value']-self.ModelParams['NT.T1']['value']
            #print epoch, self.ModelParams['T0.T1']['value'],\
                         #self.ModelParams['T0.'+TT]['value'],\
                         #self.ModelParams['T0.'+TT]['value']-(P*(epoch-TTnum)), TTnum
            for i in range(len(self.DetrendedData[TT]['x'])):
                timeStr0 = format(self.DetrendedData[TT]['x'][i],'.7f')
                #timeStr1 = format(self.DetrendedData[TT]['x'][i]-(P*(epoch-TTnum)),'.7f')
                FluxStr = format(self.DetrendedData[TT]['y'][i],'.12f')
                FluxStrErr = format(self.DetrendedData[TT]['yerr'][i],'.12f')
                lineStr0 = timeStr0+' '+FluxStr+' '+FluxStrErr
                lineStr1 = timeStr0+' '+FluxStr+' '+FluxStrErr
                print >> LCOutFile, lineStr0
                print >> ALLOutFile, lineStr1
            if TTnum != TTcount-1 :
                print >> ALLOutFile, '-1.0000000    -1.000000      -1.00000'

        ALLOutFile.close()

class PlotPrep:
    
    def __init__(self, Object):
    
        self.Object = Object
    
    def initLCPlotData(self):

        OutX = {}
        for TT in self.Object.ObservedData.keys():
            if TT.startswith('T'):
                xobs = np.array(self.Object.ObservedData[TT]['x']) -\
                                self.Object.ModelParams['T0.'+TT]['value']
                yobs = np.array(self.Object.ObservedData[TT]['y'])
                yerrobs = np.array(self.Object.ObservedData[TT]['yerr'])
                ydt = np.array(self.Object.DetrendedData[TT]['y'])
                yerrdt = np.array(self.Object.DetrendedData[TT]['yerr'])
                ymod = np.array(self.Object.ModelData[TT]['y'])
                xhimod = np.array(self.Object.HiResModelData[TT]['x']) -\
                                  self.Object.ModelParams['T0.'+TT]['value']
                yhimod = np.array(self.Object.HiResModelData[TT]['y'])
    
                OutX[TT] = {'x':xobs,'yobs':yobs,'yerrobs':yerrobs,'ydt':ydt,\
                            'yerrdt':yerrdt,'ymod':ymod,\
                            'xhiresmod':xhimod,'yhiresmod':yhimod}

        self.PlotData = OutX

    def initMCMCPlot(self,ParList,**kwargs):

        xpars = ParList[:-1]
        ypars = ParList[::-1][:-1]

        for key in kwargs:
            if key.lower() == 'ypars':
                xpars = ParList
                ypars = kwargs[key]
            if key.lower() == 'useshort':
                if kwargs[key]:
                    FileRoot = self.Object.name+'.'+self.Object.case+\
                               '.'+self.Object.fitNum+'.crop.mcmc'
                    DerFileRoot = self.Object.name+'.'+self.Object.case+\
                                '.'+self.Object.fitNum+'.mcmc.derived.crop.mcmc'
                    self.Object.CroppedFileName = MainPath+'/croppedSamples/'+FileRoot
                    self.Object.CroppedDerivedFile = MainPath+'/croppedSamples/'+DerFileRoot

        self.xpars = xpars
        self.ypars = ypars
        self.Grid = tmcmc.plotmcmc.SimplifyGrid(xpars,ypars)
        self.MCMCFiles = [self.Object.CroppedFileName,self.Object.CroppedDerivedFile]
        self.ErrorFiles = [self.Object.ParErrorFile,self.Object.DerivedErrorFile]
        self.triplot = tmcmc.plotmcmc.triplot(self.Grid,self.MCMCFiles,self.xpars,self.ypars)

    def OtherFits(self,FitNameList):

        errParDict = {}
        print FitNameList
        for Case in FitNameList:
            X = Object(self.Object.name)
            parErrPlot = {}
            try:
                X.InitiateCase(Case)
                X.InitiateFitNum(self.Object.fitNum)
                parErr = tmcmc.iopostmcmc.readErrorFile(X.ParErrorFile)
                ParErr = tmcmc.plotTransit.parErr4Plot(parErr)
                parErrPlot = tmcmc.plotTransit.parTimeDay2Sec(ParErr,self.Object.ModelParams)
            except:
                try:
                    X.InitiateTAP()
                    if len(X.FitTables.keys()) == 0:
                        raise
                    else:
                        X.setErrorFile()
                        parErr = tmcmc.iopostmcmc.readErrorFile(X.ParErrorFile)
                        ParErr = tmcmc.plotTransit.parErr4Plot(parErr)
                        parErrPlot = \
                        tmcmc.plotTransit.parTimeDay2Sec(ParErr,self.Object.ModelParams)
                except:
                    try:
                        X.OtherFitFiles(Case)
                        parErr = tmcmc.iopostmcmc.readErrorFile(X.ParErrorFile)
                        ParErr = tmcmc.plotTransit.parErr4Plot(parErr)
                        parErrPlot = ParErr
                    except:
                        raise NameError('All tries of fits failed')

            fitLabel,mtype,mcolor = tmcmc.plotTransit.FitLabels(Case)
            errParDict[Case] = {'pdict':parErrPlot,\
                                'fitLabel':fitLabel,'mtype':mtype,\
                                'mcolor':mcolor}

        if len(errParDict.keys()) > 0:
            self.OtherParErr = errParDict

    #def initOCPlot(self, **kwargs):
        
        #TTdictionary = {}
        #for 

class chainPrep:

    def __init__(self,Object,**kwargs):

        self.ObservedData = tmcmc.mcmc.ReadMultiList(Object.lcFileList)
        self.NuisanceData = tmcmc.mcmc.ReadDetrendFile(Object.nuisONOFF)
        self.BoundParams = Object.BoundParams
        self.ModelParams = Object.ModelParams
        self.FuncName = Object.FuncName
        self.ObjectName = Object.name
        self.CaseID = Object.case
        self.MainPath = MainPath
        self.ModelParams0 = MakeStartParams(Object.name,Object.fitID)

    def setForExplore(self,ParamName):

        self.ModelParams = SwitchClosedAll(self.ModelParams0)
        self.ModelParams[ParamName]['open'] = True
