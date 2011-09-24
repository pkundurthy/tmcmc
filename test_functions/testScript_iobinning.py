
import tmcmc

infile = 'XO2_2011JAN30.AP46.data'
ITime = 55591.7e0 - 0.059071812064e0 
ETime = 55591.7e0 + 0.059071812064e0
Ddict, Hdict = tmcmc.iobinning.ReadData(infile)
tmcmc.iobinning.WriteLightCurveFile('iobinning.LC.TEST1',infile,ITime,ETime)
tmcmc.iobinning.WriteNuisanceFile('iobinning.NUS.TEST1',infile)
#tmcmc.iobinning.WriteLCNUSoutlierRejection('iobinning.TEST2',infile,ITime,ETime)

