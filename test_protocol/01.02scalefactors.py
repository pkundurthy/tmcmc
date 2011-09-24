import tmcmc
from tmcmc.myfunc import *

ObservedData = tmcmc.mcmc.ReadMultiList('prescaled_lclist.ls')
NuisanceData = tmcmc.mcmc.ReadDetrendFile('PRESC.NUS.ONOFF.data')
ModelParams = tmcmc.mcmc.ReadStartParams('START.data')
##BoundParams = tmcmc.mcmc.ReadBoundsFile('BOUNDS.data')
func = 'MTQ_multidepth_tduration'
exec "ModelData = %s(ModelParams,ObservedData)" % (func)
DetrendedData = tmcmc.mcmc.DetrendData(ObservedData,ModelData,NuisanceData,None,False)

Npar = 0
for par in ModelParams.keys():
    if ModelParams[par]['open']:
        Npar += 1

OutScaledFile = open('XO2.scalefactors.data','w')
shift = 0.0
for TT in DetrendedData.keys():
    yt = []
    if TT != 'all':
        indata = DetrendedData[TT]['y'] - ModelData[TT]['y'] 
        xread = ObservedData[TT]['x']
        yread = ObservedData[TT]['y']
        yerr_obs_read = ObservedData[TT]['yerr']
        crap1, crap2, ngood, goodindex, badindex = tmcmc.binning.MedianMeanOutlierRejection(indata,5e0,'MEDIAN')
        for j in goodindex:
            if DetrendedData[TT]['yerr'][j] < 0.005:
                yt.append(((DetrendedData[TT]['y'][j]-ModelData[TT]['y'][j])/DetrendedData[TT]['yerr'][j])**2)
        scale =  np.sqrt(np.sum(yt)/(len(yt)-(Npar-len(ModelData.keys())+1)))
        print TT,' | ', scale, len(goodindex), len(DetrendedData[TT]['y'])
        NuisanceFileObject = open(NuisanceData[TT]['filename'],'r')
        NuisanceFileObject = NuisanceFileObject.readlines()
        OutFile = open('sc.LIGHTCURVE.XO2.'+TT+'.data','w')
        OutNusFile = open('sc.NUISANCE.XO2.'+TT+'.data','w')
        print >> OutScaledFile, TT, ' | ', scale
        print >> OutFile, '# BJD   | flux ratio  | errors'
        print >> OutNusFile, NuisanceFileObject[0].strip('\n')
        for j in goodindex:
            DetrendedData[TT]['yerr'][j] = scale*DetrendedData[TT]['yerr'][j]
            if DetrendedData[TT]['yerr'][j] < 0.005:
                print >> OutFile, ObservedData[TT]['x'][j],' | ',ObservedData[TT]['y'][j],' | ',DetrendedData[TT]['yerr'][j]
                print >> OutNusFile, NuisanceFileObject[j+1].strip('\n')
        OutFile.close()
        OutNusFile.close()
OutScaledFile.close()