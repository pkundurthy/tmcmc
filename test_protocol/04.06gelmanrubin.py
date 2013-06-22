
import tmcmc

#FileList = ['RUN.00001.XO2.chain001.mcmc','RUN.00002.XO2.chain001.mcmc']
FileList = ['shortChain1.mcmc','shortChain2.mcmc','shortChain3.mcmc']
ModelFile = 'START.GRTEST.data'

GRFile = 'GRStats.data'

tmcmc.postmcmc.GelmanRubinConvergence(FileList,ModelFile,GRFile,lastn=10000)