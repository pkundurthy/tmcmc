import tmcmc

x = tmcmc.iopostmcmc.readDTfile('DTCOEFF.MCMC.TEST.mcmc','NUS.ONOFF.data')

ObservedData = tmcmc.mcmc.ReadMultiList('lclist.ls')
ModelParams = tmcmc.iomcmc.ReadStartParams('STARTPARAMS.TEST.data')
FuncName = 'MTQ_multidepth_tduration'
NuisanceData = tmcmc.mcmc.ReadDetrendFile('NUS.ONOFF.data')

y = tmcmc.iopostmcmc.generateDT('MCMC.TEST.mcmc',\
    ObservedData,ModelParams,NuisanceData,FuncName)

#print y[1]['T1'].keys()
parlist = []
for num in x.keys():
    for tag in x[num].keys():
        for par in x[num][tag].keys():
            fracdiff = abs(x[num][tag][par]-y[num][tag][par])\
            /abs(max([x[num][tag][par],y[num][tag][par]]))
            if fracdiff > 0.01: 
                parlist.append(par)
                print num, tag, par, fracdiff, abs(x[num][tag][par]), abs(y[num][tag][par])
            else:
                pass

for par in x[1]['T1'].keys():
    count = 0
    for el in parlist:
        if el == par:
            count += 1
    print par, count