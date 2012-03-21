
import os
import sys
import tmcmc
import random
import numpy as np
import cPickle as cP

MainPath = '/astro/store/student-scratch1/pkundurthy/final_apostle/'
PicklePath = MainPath+'PickleStuff/'
ObjectList = ['WASP2','XO2','TRES3','GJ1214']
DataPrepPath = MainPath+'DataPrep/'
FigurePath = MainPath+'OtherFigures/'
PaperFiguresPath = MainPath+'PaperFigures/'


#FitType
DateStrings =  cP.load(open(PicklePath+'DateInfo.pickle','rb'))
ParDict = cP.load(open(PicklePath+'MCMC_MINUIT_StartInfo.pickle','rb'))
ExpectedTT = cP.load(open(PicklePath+'ExpectedTT.pickle','rb'))
#FirstOptAp = cP.load(open(PicklePath+'OptApGuess.pickle','rb'))
BoundPars = cP.load(open(PicklePath+'BoundPar.pickle','rb'))
FuncName = 'MTQ_multidepth_tduration'

CaseList = ['MCMC.FLD','MCMC.OLD','MCMC.MDFLD',\
            'MINUIT.FLD','MINUIT.OLD','MINUIT.MDFLD','MINUIT.FIRSTTRY']

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

class Object:

    def __init__(self, name):

        self.name = name
        self.ParDict = ParDict[self.name]
        self.TT = ExpectedTT[self.name]
        self.Dates = DateStrings[self.name]
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
                                  
        self.ErrorFile = self.casePath+self.name+'.'+\
                         self.case+'.'+self.fitNum+'.'+\
                         self.fitMethod+'.err'
        
        self.ErrorDerivedFile = self.casePath+self.name+'.'+\
                                self.case+'.'+self.fitNum+'.'+\
                                self.fitMethod+'.derived.err'
        
        if self.fitMethod.lower() == 'mcmc':

            self.OutFitFile = self.casePath+self.name+'.'+\
                              self.case+'.'+self.fitNum+'.'+\
                              self.fitMethod
                              
            self.CroppedFileName = self.casePath+self.name+'.'+\
                                self.case+'.'+self.fitNum+'.crop.'+\
                                self.fitMethod
                                
            self.AutoCorStatsFile = self.casePath+self.name+'.'+\
                                    self.case+'.'+self.fitNum+'.AutoCorStat'
                                    
            self.AutoCorFigRoot = self.casePath+self.name+'.'+\
                                  self.case+'.'+self.fitNum+'.AutoCorFit.'
            
            self.TracePlotRoot = self.casePath+self.name+'.'+\
                                 self.case+'.'+self.fitNum+'.TracePlot.'
                                  
            self.CovCorStatsRoot = self.casePath+self.name+'.'+\
                                   self.case+'.'+self.fitNum+'.CovCorStat'
            
            self.LowestChiSQFile = self.casePath+self.name+'.'+\
                                   self.case+'.'+self.fitNum+'.lowchisq.par'
                                   
            self.DerivedFile = self.casePath+self.name+'.'+\
                               self.case+'.'+self.fitNum+'.'+\
                               self.fitMethod+'.derived.'+self.fitMethod
                               
            self.CroppedDerivedFile = self.casePath+self.name+'.'+\
                                      self.case+'.'+self.fitNum+'.'+\
                                      self.fitMethod+'.derived.crop.'+self.fitMethod
            
            self.DerivedCovCorStatsRoot = self.casePath+self.name+'.'+\
                                          self.case+'.'+self.fitNum+'.derived.CovCorStat'

            self.DerivedLowestChiSQFile = self.casePath+self.name+'.'+\
                                          self.case+'.'+self.fitNum+'.lowchisq.derived.par'

        if self.fitMethod.lower() == 'minuit': 

            self.OutFitFile = self.casePath+self.name+'.'+\
                              self.case+'.'+self.fitNum+'.'+\
                              self.fitMethod+'.par'
 
            self.DerivedFile = self.casePath+self.name+'.'+\
                               self.case+'.'+self.fitNum+'.'+\
                               self.fitMethod+'.derived.'+self.fitMethod+'.par'

    def InitiateData(self):

        self.ObservedData = tmcmc.mcmc.ReadMultiList(self.lcFileList)
        self.NuisanceData = tmcmc.mcmc.ReadDetrendFile(self.nuisONOFF)
        exec(self.FuncExecString % self.FuncName)
        self.ModelData = ModelFunc(self.ModelParams,self.ObservedData)
        self.DetrendedData = tmcmc.mcmc.DetrendData(self.ObservedData,self.ModelData,self.NuisanceData,'',False)
        
    def MakeBoundFile(self):
        """         """

        OutFile = open(self.BoundFile,'w')
        print >> OutFile, '# Bound Func  |  Flag '
        for key in self.BoundParams.keys():
            print >> OutFile, key,' | ',self.BoundParams[key]['open']
        OutFile.close()
        
    def MakeStartFile(self, Shift):
        """         """
        
        StartParams = self.ModelParams
        #Bound0 = tmcmc.mcmc.ApplyBounds(self.ModelParams,self.BoundParams)
        Bound = False
        Trial = 1
        #print self.ModelParams.keys()
        #print Bound0
        while not Bound:
            if Trial%15 == 0:
                Shift /= 2e0
            StartParams = ApplyShift(self.ModelParams,self.fitNum,Shift)
            #print Bound, Bound0, Trial, Shift, Trial%10
            Bound = tmcmc.mcmc.ApplyBounds(StartParams,self.BoundParams)
            #print 'here 2'
            Trial += 1
            #print Bound, Bound0, Trial, Shift, Trial%10

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
                        print par+' has stabilized, acr = '+format(data['acr'][-1],'.2f')+' frac = '+str(medfrac)+' | '+self.name+', '+self.case
                        step[par] = {'frac':medfrac}
            else:
                for par in data.keys():
                    if not tmcmc.iopostmcmc.isNonParam(par):
                        print par+' has NOT stabilized, acr = '+format(data['acr'][-1],'.2f')+' | '+self.name+', '+self.case
    
        for par in step.keys():
            for key in self.ModelParams.keys():
                if key == par:
                    self.ModelParams[par]['step'] = self.ModelParams[par]['step']*step[par]['frac']
                    self.ModelParams[par]['open'] = True

    def UpdateModelParams(self):

        self.ModelParams = tmcmc.iomcmc.ReadStartParams(self.OutFitFile)

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

    def PlotPrep(self):
        
        OutX = {}
        for TT in self.ObservedData.keys():
            if TT.startswith('T'):
                xobs = np.array(self.ObservedData[TT]['x']) - self.ModelParams['T0.'+TT]['value']
                yobs = np.array(self.ObservedData[TT]['y'])
                yerrobs = np.array(self.ObservedData[TT]['yerr'])
                ydt = np.array(self.DetrendedData[TT]['y'])
                yerrdt = np.array(self.DetrendedData[TT]['yerr'])
                ymod = np.array(self.ModelData[TT]['y'])
                xhimod = np.array(self.HiResModelData[TT]['x']) - self.ModelParams['T0.'+TT]['value']
                yhimod = np.array(self.HiResModelData[TT]['y'])
                
                OutX[TT] = {'x':xobs,'yobs':yobs,'yerrobs':yerrobs,'ydt':ydt,'yerrdt':yerrdt,'ymod':ymod,\
                            'xhiresmod':xhimod,'yhiresmod':yhimod}
         
        self.PlotData = OutX
        
    def printDetrendedData(self):
        """             """
        
        self.DetrendedDataPath = MainPath+self.name+'/TAP/'
        for TT in self.DetrendedData.keys():
            if TT.startswith('T'):
                FileName = self.DetrendedDataPath+self.name+'.'+TT+'.lcdtx'
                LCOutFile = open(FileName,'w')
                print 'writing '+FileName
                #print >> LCOutFile, '# BJD   |   flux   |   err_flux '
                for i in range(len(self.DetrendedData[TT]['x'])):
                    timeStr = format(self.DetrendedData[TT]['x'][i],'.7f')
                    FluxStr = format(self.DetrendedData[TT]['y'][i],'.12f')
                    FluxStrErr = format(self.DetrendedData[TT]['yerr'][i],'.12f')
                    lineStr = timeStr+','+FluxStr+','+FluxStrErr
                    print >> LCOutFile, lineStr

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
        