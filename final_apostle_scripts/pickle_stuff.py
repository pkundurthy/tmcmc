import cPickle as pickle
from tmcmc import class_fitprep as cfp

UTD_List = {
            'WASP2':{'T1':'2007JUL24','T2':'2007JUL26','T3':'2007OCT16',\
                     'T4':'2008JUN14','T5':'2008SEP04','T6':'2008OCT02',\
                     'T7':'2008OCT30','T8':'2010JUL04','T9':'2010SEP11',\
                     'T10':'2010OCT09'},\
             'XO2': {'T1':'2008JAN08','T2':'2008FEB11','T3':'2008MAR03',\
                     'T4':'2008NOV22','T5':'2009FEB06','T6':'2009MAR12',\
                     'T7':'2010OCT25','T8':'2010DEC27','T9':'2011JAN30',\
                     'T10':'2011MAR05'},\
             'TRES3':
                    {'T1':'2009MAY14','T2':'2009JUN13','T3':'2010MAR22',\
                     'T4':'2010MAY16','T5':'2010JUN02','T6':'2010OCT12',\
                     'T7':'2011MAR24','T8':'2011APR27','T9':'2011MAY14',\
                     'T10':'2011JUN21','T11':'2011AUG24'},\
             'GJ1214':
                    {'T1':'2010APR21','T2':'2010JUN06','T3':'2010JUL06',\
                     'T4':'2011MAY26','T5':'2011JUN25','T6':'2011AUG02'}
            }


fileOut = open(cfp.PicklePath+'DateInfo.pickle','wb')
pickle.dump(UTD_List,fileOut,-1)
fileOut.close()

UTD_DateString = {
            'WASP2':{'T1':'2007-07-24','T2':'2007-07-26','T3':'2007-10-16',\
                     'T4':'2008-06-14','T5':'2008-09-04','T6':'2008-10-02',\
                     'T7':'2008-10-30','T8':'2010-07-04','T9':'2010-09-11',\
                     'T10':'2010-10-09'},\
             'XO2': {'T1':'2008-01-08','T2':'2008-02-11','T3':'2008-03-03',\
                     'T4':'2008-09-22','T5':'2009-02-06','T6':'2009-03-12',\
                     'T7':'2010-10-25','T8':'2010-12-27','T9':'2011-01-30',\
                     'T10':'2011-03-05'},\
             'TRES3':
                    {'T1':'2009-05-14','T2':'2009-06-13','T3':'2010-03-22',\
                     'T4':'2010-05-16','T5':'2010-06-02','T6':'2010-10-12',\
                     'T7':'2011-03-24','T8':'2011-04-27','T9':'2011-05-14',\
                     'T10':'2011-06-21','T11':'2011-08-24'},\
             'GJ1214':
                    {'T1':'2010-04-21','T2':'2010-06-06','T3':'2010-07-06',\
                     'T4':'2011-05-26','T5':'2011-06-25','T6':'2011-08-02'}
            }

fileOut = open(cfp.PicklePath+'DateString.pickle','wb')
pickle.dump(UTD_DateString,fileOut,-1)
fileOut.close()

StartDict = {
            'WASP2':{
                'f0': {'step': 0.0, 'printformat': '.7f', 'open': False, 'value': 1.0},\
                'tG': {'step': 0.0001799, 'printformat': '.7f', 'open': True, 'value': 0.0176421},\
                'tT': {'step': 0.0001222, 'printformat': '.7f', 'open': True, 'value': 0.0577678},\
                'T0.T1': {'step': 0.000416991, 'printformat': '.9f', 'open': True, 'value': 54305.7381936},\
                'T0.T2': {'step': 0.000316622, 'printformat': '.9f', 'open': True, 'value': 54307.8919863},\
                'T0.T3': {'step': 0.00015009, 'printformat': '.9f', 'open': True, 'value': 54389.6760604},\
                'T0.T4': {'step': 0.000151223, 'printformat': '.9f', 'open': True, 'value': 54632.8773402},\
                'T0.T5': {'step': 0.00023359, 'printformat': '.9f', 'open': True, 'value': 54714.6615282},\
                'T0.T6': {'step': 0.000143349, 'printformat': '.9f', 'open': True, 'value': 54742.6400723},\
                'T0.T7': {'step': 0.000173906, 'printformat': '.9f', 'open': True, 'value': 54770.6190792},\
                'T0.T8': {'step': 0.001217086, 'printformat': '.9f', 'open': True, 'value': 55381.8514687},\
                'T0.T9': {'step': 0.000207094, 'printformat': '.9f', 'open': True, 'value':55450.7213718},\
                'T0.T10': {'step': 0.00012603, 'printformat': '.9f', 'open': True, 'value': 55478.7017604},\
                'v1.T1.T2.T3.T4.T5.T6.T7': {'step': 0.01, 'printformat': '.4f', 'open': False, 'value': 0.6092},\
                'u1.T1.T2.T3.T4.T5.T6.T7': {'step': 0.01, 'printformat': '.4f', 'open': False, 'value': 0.3926},\
                'v2.T1.T2.T3.T4.T5.T6.T7': {'step': 0.01, 'printformat': '.4f', 'open': False, 'value': 0.176},\
                'u2.T1.T2.T3.T4.T5.T6.T7': {'step': 0.01, 'printformat': '.4f', 'open': False, 'value': 0.2166},\
                'v1.T8.T9.T10': {'step': 0.01, 'printformat': '.4f', 'open': False, 'value': 0.7135},\
                'u1.T8.T9.T10': {'step': 0.01, 'printformat': '.4f', 'open': False, 'value': 0.5541},\
                'v2.T8.T9.T10': {'step': 0.01, 'printformat': '.4f', 'open': False, 'value': 0.3947},\
                'u2.T8.T9.T10': {'step': 0.01, 'printformat': '.4f', 'open': False, 'value': 0.1594},\
                'D.T1.T2.T3.T4.T5.T6.T7' : {'step': 0.0005, 'printformat': '.7f', 'open': True, 'value': 0.013},\
                'D.T8.T9.T10'            : {'step': 0.0005, 'printformat': '.7f', 'open': True, 'value': 0.014},\
                'D.T1': {'step': 0.0005, 'printformat': '.7f', 'open': True, 'value': 0.013},\
                'D.T2': {'step': 0.0005, 'printformat': '.7f', 'open': True, 'value': 0.014},\
                'D.T3': {'step': 0.0005, 'printformat': '.7f', 'open': True, 'value': 0.015},\
                'D.T4': {'step': 0.0005, 'printformat': '.7f', 'open': True, 'value': 0.016},\
                'D.T5': {'step': 0.0005, 'printformat': '.7f', 'open': True, 'value': 0.011},\
                'D.T6': {'step': 0.0005, 'printformat': '.7f', 'open': True, 'value': 0.012},\
                'D.T7': {'step': 0.0005, 'printformat': '.7f', 'open': True, 'value': 0.014},\
                'D.T8': {'step': 0.0005, 'printformat': '.7f', 'open': True, 'value': 0.015},\
                'D.T9': {'step': 0.0005, 'printformat': '.7f', 'open': True, 'value': 0.012},\
                'D.T10': {'step': 0.0005, 'printformat': '.7f', 'open': True, 'value': 0.011},\
                'NT.T1': {'step': 0.0, 'printformat': 'n', 'open': False, 'value': -272.0},\
                'NT.T2': {'step': 0.0, 'printformat': 'n', 'open': False, 'value': -271.0},\
                'NT.T3': {'step': 0.0, 'printformat': 'n', 'open': False, 'value': -233.0},\
                'NT.T4': {'step': 0.0, 'printformat': 'n', 'open': False, 'value': -120.0},\
                'NT.T5': {'step': 0.0, 'printformat': 'n', 'open': False, 'value': -82.0},\
                'NT.T6': {'step': 0.0, 'printformat': 'n', 'open': False, 'value': -69.0},\
                'NT.T7': {'step': 0.0, 'printformat': 'n', 'open': False, 'value': -56.0},\
                'NT.T8': {'step': 0.0, 'printformat': 'n', 'open': False, 'value': 228.0},\
                'NT.T9': {'step': 0.0, 'printformat': 'n', 'open': False, 'value': 260.0},\
                'NT.T10': {'step': 0.0, 'printformat': 'n', 'open': False, 'value': 273.0},\
                'RefFilt': {'step': 0.0, 'printformat': ['T1.T2.T3.T4.T5.T6.T7','T6'], 'open': False, 'value': 'nan'}\
                    },\
            'XO2':{
                'f0': {'step': 0.0, 'printformat': '.7f', 'open': False, 'value': 1.0},\
                'tG': {'step': 0.0005, 'printformat': '.7f', 'open': True, 'value': 0.0176421},\
                'tT': {'step': 0.00017, 'printformat': '.7f', 'open': True, 'value': 0.0577678},\
                'T0.T1': {'step': 0.0004161, 'printformat': '.9f', 'open': True, 'value': 54474.72877},\
                'T0.T2': {'step': 0.0003162, 'printformat': '.9f', 'open': True, 'value': 54508.73466},\
                'T0.T3': {'step': 0.0001592, 'printformat': '.9f', 'open': True, 'value': 54529.66137},\
                'T0.T4': {'step': 0.0001512, 'printformat': '.9f', 'open': True, 'value': 54793.86500},\
                'T0.T5': {'step': 0.0002339, 'printformat': '.9f', 'open': True, 'value': 54869.72700},\
                'T0.T6': {'step': 0.0001439, 'printformat': '.9f', 'open': True, 'value': 54903.73500},\
                'T0.T7': {'step': 0.0001739, 'printformat': '.9f', 'open': True, 'value': 55494.91900},\
                'T0.T8': {'step': 0.0012171, 'printformat': '.9f', 'open': True, 'value': 55557.70000},\
                'T0.T9': {'step': 0.0002074, 'printformat': '.9f', 'open': True, 'value': 55591.70500},\
                'T0.T10': {'step': 0.0001262, 'printformat': '.9f', 'open': True, 'value': 55625.71000},\
                'v1.T1.T2.T3.T4.T5.T6': {'step': 0.01, 'printformat': '.4f', 'open': False, 'value': 0.5944},\
                'u1.T1.T2.T3.T4.T5.T6': {'step': 0.01, 'printformat': '.4f', 'open': False, 'value': 0.3698},\
                'v2.T1.T2.T3.T4.T5.T6': {'step': 0.01, 'printformat': '.4f', 'open': False, 'value': 0.1452},\
                'u2.T1.T2.T3.T4.T5.T6': {'step': 0.01, 'printformat': '.4f', 'open': False, 'value': 0.2246},\
                'v1.T7.T8.T9.T10': {'step': 0.01, 'printformat': '.4f', 'open': False, 'value': 0.6980},\
                'u1.T7.T8.T9.T10': {'step': 0.01, 'printformat': '.4f', 'open': False, 'value': 0.5252},\
                'v2.T7.T8.T9.T10': {'step': 0.01, 'printformat': '.4f', 'open': False, 'value': 0.3524},\
                'u2.T7.T8.T9.T10': {'step': 0.01, 'printformat': '.4f', 'open': False, 'value': 0.1728},\
                'D.T1.T2.T3.T4.T5.T6': {'step': 0.0005, 'printformat': '.7f', 'open': True, 'value': 0.013},\
                'D.T7.T8.T9.T10': {'step': 0.0005, 'printformat': '.7f', 'open': True, 'value': 0.014},\
                'D.T1': {'step': 0.0005, 'printformat': '.7f', 'open': True, 'value': 0.013},\
                'D.T2': {'step': 0.0005, 'printformat': '.7f', 'open': True, 'value': 0.014},\
                'D.T3': {'step': 0.0005, 'printformat': '.7f', 'open': True, 'value': 0.015},\
                'D.T4': {'step': 0.0001, 'printformat': '.7f', 'open': True, 'value': 0.015},\
                'D.T5': {'step': 0.0005, 'printformat': '.7f', 'open': True, 'value': 0.011},\
                'D.T6': {'step': 0.0005, 'printformat': '.7f', 'open': True, 'value': 0.012},\
                'D.T7': {'step': 0.0005, 'printformat': '.7f', 'open': True, 'value': 0.014},\
                'D.T8': {'step': 0.0005, 'printformat': '.7f', 'open': True, 'value': 0.015},\
                'D.T9': {'step': 0.0005, 'printformat': '.7f', 'open': True, 'value': 0.012},\
                'D.T10': {'step': 0.0005, 'printformat': '.7f', 'open': True, 'value': 0.011},\
                'NT.T1': {'step': 0.0, 'printformat': 'n', 'open': False, 'value': -265.0},\
                'NT.T2': {'step': 0.0, 'printformat': 'n', 'open': False, 'value': -252.0},\
                'NT.T3': {'step': 0.0, 'printformat': 'n', 'open': False, 'value': -244.0},\
                'NT.T4': {'step': 0.0, 'printformat': 'n', 'open': False, 'value': -143.0},\
                'NT.T5': {'step': 0.0, 'printformat': 'n', 'open': False, 'value': -114.0},\
                'NT.T6': {'step': 0.0, 'printformat': 'n', 'open': False, 'value': -101.0},\
                'NT.T7': {'step': 0.0, 'printformat': 'n', 'open': False, 'value': 125.0},\
                'NT.T8': {'step': 0.0, 'printformat': 'n', 'open': False, 'value': 149.0},\
                'NT.T9': {'step': 0.0, 'printformat': 'n', 'open': False, 'value': 162.0},\
                'NT.T10': {'step': 0.0, 'printformat': 'n', 'open': False, 'value': 175.0},\
                'RefFilt': {'step': 0.0, 'printformat': ['T1.T2.T3.T4.T5.T6','T4'], 'open': False, 'value': 'nan'}\
                },\
            'TRES3':{
                'f0': {'step': 0.0, 'printformat': '.7f', 'open': False, 'value': 1.0},\
                'NT.T1': {'step': 0.0, 'printformat': '.1f', 'open': False, 'value': 0.0},\
                'NT.T2': {'step': 0.0, 'printformat': '.1f', 'open': False, 'value': 23.0},\
                'NT.T3': {'step': 0.0, 'printformat': '.1f', 'open': False, 'value': 239.0},\
                'NT.T4': {'step': 0.0, 'printformat': '.1f', 'open': False, 'value': 281.0},\
                'NT.T5': {'step': 0.0, 'printformat': '.1f', 'open': False, 'value': 294.0},\
                'NT.T6': {'step': 0.0, 'printformat': '.1f', 'open': False, 'value': 395.0},\
                'NT.T7': {'step': 0.0, 'printformat': '.1f', 'open': False, 'value': 520.0},\
                'NT.T8': {'step': 0.0, 'printformat': '.1f', 'open': False, 'value': 546.0},\
                'NT.T9': {'step': 0.0, 'printformat': '.1f', 'open': False, 'value': 559.0},\
                'NT.T10': {'step': 0.0, 'printformat': '.1f', 'open': False, 'value': 588.0},\
                'NT.T11': {'step': 0.0, 'printformat': '.1f', 'open': False, 'value': 637.0},\
                'T0.T1': {'step': 0.0001996, 'printformat': '.7f', 'open': True, 'value': 54965.70553},\
                'T0.T2': {'step': 0.0002484, 'printformat': '.7f', 'open': True, 'value': 54995.74790},\
                'T0.T3': {'step': 0.0004301, 'printformat': '.7f', 'open': True, 'value': 55277.88494},\
                'T0.T4': {'step': 0.000155, 'printformat': '.7f', 'open': True, 'value': 55332.744930},\
                'T0.T5': {'step': 0.0015295, 'printformat': '.7f', 'open': True, 'value': 55349.72539},\
                'T0.T6': {'step': 0.0002386, 'printformat': '.7f', 'open': True, 'value': 55481.65058},\
                'T0.T7': {'step': 0.0001518, 'printformat': '.7f', 'open': True, 'value': 55644.92433},\
                'T0.T8': {'step': 0.0002433, 'printformat': '.7f', 'open': True, 'value': 55678.88527},\
                'T0.T9': {'step': 0.0002145, 'printformat': '.7f', 'open': True, 'value': 55695.86574},\
                'T0.T10': {'step': 0.0001806, 'printformat': '.7f', 'open': True, 'value': 55733.74525},\
                'T0.T11': {'step': 0.0002813, 'printformat': '.7f', 'open': True, 'value': 55797.74856},\
                'D.T1': {'step': 0.0004504, 'printformat': '.7f', 'open': True, 'value': 0.025},\
                'D.T2': {'step': 0.0011122, 'printformat': '.7f', 'open': True, 'value': 0.025},\
                'D.T3': {'step': 0.0009062, 'printformat': '.7f', 'open': True, 'value': 0.025},\
                'D.T4': {'step': 0.0004051, 'printformat': '.7f', 'open': True, 'value': 0.025},\
                'D.T5': {'step': 0.0041965, 'printformat': '.7f', 'open': True, 'value': 0.025},\
                'D.T6': {'step': 0.0004954, 'printformat': '.7f', 'open': True, 'value': 0.025},\
                'D.T7': {'step': 0.0002474, 'printformat': '.7f', 'open': True, 'value': 0.025},\
                'D.T8': {'step': 0.000504, 'printformat': '.7f', 'open': True, 'value': 0.025},\
                'D.T9': {'step': 0.0005474, 'printformat': '.7f', 'open': True, 'value': 0.025},\
                'D.T10': {'step': 0.0005605, 'printformat': '.7f', 'open': True, 'value': 0.025},\
                'D.T11': {'step': 0.0005706, 'printformat': '.7f', 'open': True, 'value': 0.025},\
                'tG': {'step': 0.0002301, 'printformat': '.7f', 'open': True, 'value': 0.0202954},\
                'tT': {'step': 0.0001111, 'printformat': '.7f', 'open': True, 'value': 0.0385016},\
                'D.T1.T2.T3.T4.T5.T6.T7.T8.T9.T10.T11':\
                {'step': 0.0006, 'printformat': '.7f', 'open': False, 'value': 0.025},\
                'v1.T1.T2.T3.T4.T5.T6.T7.T8.T9.T10.T11':\
                {'step': 0.01, 'printformat': '.4f', 'open': False, 'value': 0.67675},\
                'v2.T1.T2.T3.T4.T5.T6.T7.T8.T9.T10.T11':\
                {'step': 0.01, 'printformat': '.4f', 'open': False, 'value': 0.30075},\
                'u1.T1.T2.T3.T4.T5.T6.T7.T8.T9.T10.T11':\
                {'step': 0.01, 'printformat': '.4f', 'open': False, 'value': 0.48875},\
                'u2.T1.T2.T3.T4.T5.T6.T7.T8.T9.T10.T11':\
                {'step': 0.01, 'printformat': '.4f', 'open': False, 'value': 0.1880},\
                'RefFilt': {'step': 0.0, 'printformat': ['T1.T2.T3.T4.T5.T6.T7.T8.T9.T10.T11','T7'], 'open': False, 'value': 'nan'}\
                },\
            'GJ1214':{\
                'f0': {'step': 0.0, 'printformat': '.7f', 'open': False, 'value': 1.0},\
                'NT.T1': {'step': 0.0, 'printformat': '.1f', 'open': False, 'value': 0.0},\
                'NT.T2': {'step': 0.0, 'printformat': '.1f', 'open': False, 'value': 29.0},\
                'NT.T3': {'step': 0.0, 'printformat': '.1f', 'open': False, 'value': 48.0},\
                'NT.T4': {'step': 0.0, 'printformat': '.1f', 'open': False, 'value': 253.0},\
                'NT.T5': {'step': 0.0, 'printformat': '.1f', 'open': False, 'value': 294.0},\
                'NT.T6': {'step': 0.0, 'printformat': '.1f', 'open': False, 'value': 296.0},\
                'T0.T1': {'step': 0.0001996, 'printformat': '.7f', 'open': True, 'value': 55307.8926},\
                'T0.T2': {'step': 0.0002484, 'printformat': '.7f', 'open': True, 'value': 55353.7244},\
                'T0.T3': {'step': 0.0004301, 'printformat': '.7f', 'open': True, 'value': 55383.7521},\
                'T0.T4': {'step': 0.000155, 'printformat': '.7f', 'open': True, 'value': 55707.7350},\
                'T0.T5': {'step': 0.0015295, 'printformat': '.7f', 'open': True, 'value': 55737.7627246},\
                'T0.T6': {'step': 0.0002386, 'printformat': '.7f', 'open': True, 'value': 55775.6924415},\
                'D.T1': {'step': 0.0004504, 'printformat': '.7f', 'open': True, 'value': 0.0179},\
                'D.T2': {'step': 0.0011122, 'printformat': '.7f', 'open': True, 'value': 0.0179},\
                'D.T3': {'step': 0.0009062, 'printformat': '.7f', 'open': True, 'value': 0.0179},\
                'D.T4': {'step': 0.0004051, 'printformat': '.7f', 'open': True, 'value': 0.0179},\
                'D.T5': {'step': 0.0041965, 'printformat': '.7f', 'open': True, 'value': 0.0179},\
                'D.T6': {'step': 0.0004954, 'printformat': '.7f', 'open': True, 'value': 0.0179},\
                'tG': {'step': 0.0002301, 'printformat': '.7f', 'open': True, 'value': 0.0046},\
                'tT': {'step': 0.0001111, 'printformat': '.7f', 'open': True, 'value': 0.0326},\
                'D.T1.T2.T3.T4.T5.T6':\
                {'step': 0.0006, 'printformat': '.7f', 'open': False, 'value': 0.0179},\
                'v1.T1.T2.T3.T4.T5.T6':\
                {'step': 0.01, 'printformat': '.4f', 'open': False, 'value': 0.8885},\
                'v2.T1.T2.T3.T4.T5.T6':\
                {'step': 0.01, 'printformat': '.4f', 'open': False, 'value': 0.3843},\
                'u1.T1.T2.T3.T4.T5.T6':\
                {'step': 0.01, 'printformat': '.4f', 'open': False, 'value': 0.6364},\
                'u2.T1.T2.T3.T4.T5.T6':\
                {'step': 0.01, 'printformat': '.4f', 'open': False, 'value': 0.2521},\
                'RefFilt': {'step': 0.0, 'printformat': ['T1.T2.T3.T4.T5.T6','T1'], 'open': False, 'value': 'nan'}\
                }\
            }

fileOut = open(cfp.PicklePath+'MCMC_MINUIT_StartInfo.pickle','wb')
pickle.dump(StartDict,fileOut,-1)
fileOut.close()

BoundDict = {'MTQ_multidepth_tduration':\
                {'bound_v1_2011':{'open':True},\
                 'bound_v1plusv2_2011':{'open':True},\
                 'bound_uvalues_2011':{'open':True},\
                 'bound_tG_2011':{'open':True},\
                 'bound_tT_2011':{'open':True},\
                 'bound_D_2011':{'open':True},\
                 'bound_vfraction_MTQ_2011':{'open':True},\
                 'bound_bfraction_MTQ_2011':{'open':True},\
                 'bound_bOVERaRs_MTQ_2011':{'open':True}
                 }
            }

fileOut = open(cfp.PicklePath+'BoundPar.pickle','wb')
pickle.dump(BoundDict,fileOut,-1)
fileOut.close()

ExpectedTT = {'WASP2':{
                       'T1':54305.738193600,\
                       'T2':54307.891986300,\
                       'T3':54389.676060400,\
                       'T4':54632.877340200,\
                       'T5':54714.661528200,\
                       'T6':54742.640072300,\
                       'T7':54770.619079200,\
                       'T8':55381.851468700,\
                       'T9':55450.721371800,\
                       'T10':55478.701760400},\
               'XO2':{
                      'T1':54474.728770000,\
                      'T2':54508.734660000,\
                      'T3':54529.661370000,\
                      'T4':54793.865000000,\
                      'T5':54869.727000000,\
                      'T6':54903.735000000,\
                      'T7':55494.919000000,\
                      'T8':55557.700000000,\
                      'T9':55591.705000000,\
                      'T10':55625.710000000},\
               'TRES3':{
                      'T1':54965.7055300,\
                      'T2':54995.7479000,\
                      'T3':55277.8849400,\
                      'T4':55332.7449200,\
                      'T5':55349.7253900,\
                      'T6':55481.6505800,\
                      'T7':55644.9243300,\
                      'T8':55678.8852700,\
                      'T9':55695.8657400,\
                      'T10':55733.7452500,\
                      'T11':55797.7485600},\
               'GJ1214':{
                      'T1':55307.8926,\
                      'T2':55353.7244,\
                      'T3':55383.7521,\
                      'T4':55707.7350,\
                      'T5':55737.7627246,\
                      'T6':55775.6924415}\
              }


fileOut = open(cfp.PicklePath+'ExpectedTT.pickle','wb')
pickle.dump(ExpectedTT,fileOut,-1)
fileOut.close()

FirstOptAp = {'WASP2':{
                       'T1':15,'T2':11,'T3':16, 
                       'T4':21,'T5':24,'T6':21, 
                       'T7':22,'T8':26,'T9':23, 
                       'T10':20},
               'XO2':{
                      'T1':14,'T2':16,'T3':21, 
                      'T4':14,'T5':24,'T6':31, 
                      'T7':43,'T8':36,'T9':46, 
                      'T10':44},
               'TRES3':{
                      'T1':27,'T2':19,'T3':20,
                      'T4':26,'T5':48,'T6':48,
                      'T7':20,'T8':18,'T9':19,
                      'T10':24,'T11':19},
                'GJ1214':{
                      'T1':22,'T2':22,'T3':22,
                      'T4':22,'T5':22,'T6':22}
              }

fileOut = open(cfp.PicklePath+'OptApGuess.pickle','wb')
pickle.dump(FirstOptAp,fileOut,-1)
fileOut.close()

