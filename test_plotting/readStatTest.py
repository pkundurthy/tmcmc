
import tmcmc

x = tmcmc.iopostmcmc.readALLStats(cov='COV.stat',spear='SPEAR.stat',pear='PEAR.stat')


print x['cov']['D.T1.T2.T3'].keys()