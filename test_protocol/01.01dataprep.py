
import tmcmc

infile = 'XO2_2010OCT25.AP43.data'
#ITime = 55494.919e0 - 0.059071812064e0 
#ETime = 55494.919e0 + 0.059071812064e0
Ddict, Hdict = tmcmc.iobinning.ReadData(infile)
tmcmc.iobinning.WriteLightCurveFile('PRELC.T1.data',infile,55494.860e0,55494.978e0)
tmcmc.iobinning.WriteNuisanceFile('PRENUS.T1.data',infile)

infile = 'XO2_2011JAN30.AP46.data'
#ITime = 55591.628966e0 - 0.059071812064e0 
#ETime = 55591.628966e0 + 0.059071812064e0
Ddict, Hdict = tmcmc.iobinning.ReadData(infile)
tmcmc.iobinning.WriteLightCurveFile('PRELC.T2.data',infile,55591.642,55591.768)
tmcmc.iobinning.WriteNuisanceFile('PRENUS.T2.data',infile)

infile = 'XO2_2011MAR05.AP44.data'
#ITime = 55625.63486e0 - 0.059071812064e0 
#ETime = 55625.63486e0 + 0.059071812064e0
Ddict, Hdict = tmcmc.iobinning.ReadData(infile)
tmcmc.iobinning.WriteLightCurveFile('PRELC.T3.data',infile,55625.646,55625.774)
tmcmc.iobinning.WriteNuisanceFile('PRENUS.T3.data',infile)

#tmcmc.iobinning.WriteLCNUSoutlierRejection('iobinning.TEST2',infile,ITime,ETime)
