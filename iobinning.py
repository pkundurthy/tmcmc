""" Contains various functions needed read and write files using output from the AGILE pipeline. """

import numpy as np
import tmcmc.binning as binning
import sys
if sys.version_info[1] < 6:
    from tmcmc.misc import format

def ReadData(file):
    """ Read header from datafiles. Datafiles (file) are those files output by the 
    last IDL data extraction routine in the Agile pipeline.
    Input:
        file - name of file with IDL data
    Output:
        Datadictionary - dictionary with output from photometry
        HeaderData - header keys in IDL data file
    """

    FileObject = open(file,'r')
    FileLines = FileObject.readlines()
    
    # define dictionary for header data
    HeaderData = {}
    for line in FileLines:
        if line.startswith('#'):
            line = line.strip('#')
            dummy_array = map(str,line.split('|'))
            for i in range(len(dummy_array)):
                if i == 0:
                    # assumes that column 0 is always time
                    Time_Split = map(str,dummy_array[0].split('+'))
                    HeaderData[i] = Time_Split[1].strip()
                else:
                    # stores the remaining header keys
                    HeaderData[i] = dummy_array[i].strip()
    
    # Create empty arrays in required data dictionary
    DataDictionary = {}
    for key in HeaderData.keys():
        DataDictionary[HeaderData[key]] = []

    for line in FileLines:
        if not line.startswith('#'):
            dummy_array = map(float,line.split('|'))
            for key in HeaderData.keys():
                DataDictionary[HeaderData[key]].append(dummy_array[key])
    
    DataDictionary['JDprefix'] = float(Time_Split[0].strip())
    return DataDictionary, HeaderData

def WriteLightCurveFile(OutFileName,file,IngressTime,EgressTime):
    """ Writes a Lightcurve file (usable by MCMC), normalizing the out-of-transit 
    lightcurve to 1.
    Inputs
        OutFileName - String with the name of the file to write the lightcurve
        file - String with the name of the file with Input data (IDL data file)
        IngressTime - Float with an approximate guess of the onset of Ingress
        EgressTime - Float with an approximate guess of the end of Egress
    Result - Lightcurve with out-of-eclipse data normalized to 1 is written to OutFileName
    """

    DataDictionary, HeaderData = ReadData(file)
    FileObject = open(OutFileName,'w')
    
    Nlen = len(DataDictionary['(BJD)']) 
    outdata = {'time':[],'flux_ratio':[],'err_fluxratio':[]}
    
    for i in range(Nlen):
        outdata['time'].append(DataDictionary['JDprefix']+DataDictionary['(BJD)'][i])
        if DataDictionary['f1'][i] == 0.0 or DataDictionary['f2'][i] == 0.0 or \
        DataDictionary['f1'][i] < 0.0 or DataDictionary['f2'][i] < 0.0:
            # if there is no flux data write 'nans'
            outdata['flux_ratio'].append(float('nan'))
            outdata['err_fluxratio'].append(float('nan'))
        else:
            # compute flux ratios
            outdata['flux_ratio'].append(DataDictionary['f1'][i]/DataDictionary['f2'][i])
            outdata['err_fluxratio'].append((1e0/DataDictionary['f2'][i])*\
            np.sqrt(DataDictionary['erf1sq'][i] + DataDictionary['erf2sq'][i]*\
            (DataDictionary['f1'][i]/DataDictionary['f2'][i])**2))

    flat_flux = []
    for i in range(len(outdata['time'])):
        if outdata['time'][i] < IngressTime or outdata['time'][i] > EgressTime:
            flat_flux.append(outdata['flux_ratio'][i])

    # normalize lightcurve
    normalizing_factor = np.median(np.array(flat_flux))
    print normalizing_factor
    if np.isnan(normalizing_factor):
        normalizing_factor = 1e0

    print >> FileObject, '# TDB | flux_ratio | err_fluxratio'
    for i in range(len(outdata['time'])):
        time = format(outdata['time'][i],'.9f')
        fratio = format(outdata['flux_ratio'][i]/normalizing_factor,'.7f')
        err_fratio = format(outdata['err_fluxratio'][i]/normalizing_factor,'.7f')
        print >> FileObject, time+' | '+fratio+' | '+err_fratio
    
    FileObject.close()

def WriteNuisanceFile(OutFileName,file):
    """ Writes a Nuisance Data file (usable by MCMC).
    Inputs
        OutFileName - String with the name of the file to write the nuisance data
        file - String with the name of the file with Input data (IDL data file) 

    Results
        Nuisance data is written to OutFileName
    """
    
    DataDictionary, HeaderData = ReadData(file)
    FileObject = open(OutFileName,'w')
    
    # Data and Header for non lightcurve related data
    HeaderLine = '#'
    NheaderLen = len(HeaderData.keys())
    for i in range(NheaderLen):
        if HeaderData[i] != '(BJD)' and HeaderData[i] != 'f1' \
        and HeaderData[i] != 'f2' and HeaderData[i] != 'erf1sq' \
        and HeaderData[i] != 'erf2sq' and HeaderData[i] != 'ootfg':
            HeaderLine = HeaderLine+HeaderData[i]+' | '
    HeaderLine = HeaderLine+' time | diff_sky | dist | sky_ratio1 | sky_ratio2 '
    print >> FileObject, HeaderLine.strip('| \n')
    Nlen = len(DataDictionary['(BJD)'])
    for j in range(Nlen):
        Line = ''
        for i in range(NheaderLen):
            if HeaderData[i] != '(BJD)' and HeaderData[i] != 'f1' \
            and HeaderData[i] != 'f2' and HeaderData[i] != 'erf1sq' \
            and HeaderData[i] != 'erf2sq' and HeaderData[i] != 'ootfg':
                Line = Line+str(DataDictionary[HeaderData[i]][j])+' | '
        time = str(j)
        dist = np.sqrt((DataDictionary['x1'][j]-DataDictionary['x2'][j])**2 \
        + (DataDictionary['y1'][j]-DataDictionary['y2'][j])**2)
        diff_sky = DataDictionary['msky1'][j]-DataDictionary['msky2'][j]
        sky_ratio1 = DataDictionary['msky1'][j]/DataDictionary['gsky'][j]
        sky_ratio2 = DataDictionary['msky2'][j]/DataDictionary['gsky'][j]
        Line = Line+time+' | '+str(diff_sky)+' | '+str(dist)+' | '+\
        str(sky_ratio1)+' | '+str(sky_ratio2)
        print >> FileObject, Line.strip('| \n')

    FileObject.close()

def WriteLCNUSoutlierRejection(OutFileTag,file,IngressTime,EgressTime):
    """ Writes a LC and Nuisance Data file (usable by tmcmc).
    Inputs
        OutFileName - String with the name of the file to write the nuisance data
        file - String with the name of the file with Input data (IDL data file) 

    Results
        Nuisance data is written to OutFileName
    """
    
    namesplit = map(str,file.split('.'))
    LCFileObject = open('LIGHTCURVE.'+OutFileTag+'.data','w')
    NusFileObject = open('NUISANCE.'+OutFileTag+'.data','w')
    DataDictionary, HeaderData = ReadData(file)
    outdata = {'time':[],'flux_ratio':[],'err_fluxratio':[]}
    
    Nlen = len(DataDictionary['(BJD)'])
    NheaderLen = len(HeaderData.keys())
    LineList = {}
    for i in range(Nlen):
        Line = ''
        outdata['time'].append(DataDictionary['JDprefix']+DataDictionary['(BJD)'][i])
        if DataDictionary['f1'][i] == 0.0 or DataDictionary['f2'][i] == 0.0 or \
        DataDictionary['f1'][i] < 0.0 or DataDictionary['f2'][i] < 0.0:
            # if there is no flux data write 'nans'
            outdata['flux_ratio'].append(float('+99'))
            outdata['err_fluxratio'].append(float('+99'))
        else:
            # compute flux ratios
            outdata['flux_ratio'].append(DataDictionary['f1'][i]/DataDictionary['f2'][i])
            outdata['err_fluxratio'].append((1e0/DataDictionary['f2'][i])*\
            np.sqrt(DataDictionary['erf1sq'][i] + DataDictionary['erf2sq'][i]*\
            (DataDictionary['f1'][i]/DataDictionary['f2'][i])**2))
        for j in range(NheaderLen):
            if HeaderData[j] != '(BJD)' and HeaderData[j] != 'f1' \
            and HeaderData[j] != 'f2' and HeaderData[j] != 'erf1sq' \
            and HeaderData[j] != 'erf2sq' and HeaderData[j] != 'ootfg':
                Line = Line+str(DataDictionary[HeaderData[j]][i])+' | '
        time = str(i)
        dist = np.sqrt((DataDictionary['x1'][i]-DataDictionary['x2'][i])**2 + (DataDictionary['y1'][i]-DataDictionary['y2'][i])**2)
        diff_sky = DataDictionary['msky1'][i]-DataDictionary['msky2'][i]
        sky_ratio1 = DataDictionary['msky1'][i]/DataDictionary['gsky'][i]
        sky_ratio2 = DataDictionary['msky2'][i]/DataDictionary['gsky'][i]
        Line = Line+time+' | '+str(diff_sky)+' | '+str(dist)+' | '+str(sky_ratio1)+' | '+str(sky_ratio2)
        LineList[i] = Line
    
    # normalize lightcurve
    dd = np.array(outdata['flux_ratio'])/np.median(outdata['flux_ratio'])
    #print np.isnan(dd)
    mm, sdv, ngood, goodindex, badindex = binning.MedianMeanOutlierRejection(dd,5.0,'median')
    #print mm, TT, file, np.shape(dd), np.shape(goodindex)
    import pylab
    t = np.array(outdata['time'])
    x = np.array(outdata['flux_ratio'])
    pylab.plot(t[goodindex],\
    x[goodindex], 'bo')
    pylab.plot(t[badindex],\
    x[badindex], 'ro')
    pylab.show()
    normalizing_factor = mm
    if np.isnan(normalizing_factor):
        normalizing_factor = 1e0

    for goodi in goodindex:
        time = format(outdata['time'][goodi],'.9f')
        fratio = format(outdata['flux_ratio'][goodi]/normalizing_factor,'.7f')
        err_fratio = format(outdata['err_fluxratio'][goodi]/normalizing_factor,'.7f')
        print >> LCFileObject,time+' | '+fratio+' | '+err_fratio
        print >> NusFileObject,LineList[goodi]
    LCFileObject.close()
    NusFileObject.close()