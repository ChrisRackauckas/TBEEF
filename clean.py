import os
import config
WORK_PATH = os.getcwd()

os.system("find Data/Effects ! -name README -type f -delete")
os.system("find Data/PreProcessed ! -name README -type f -delete")
os.system("find Data/ModelPredictions ! -name README -type f -delete")
os.system("find Data/ModelData ! -name README -type f -delete")
os.system("rm Data/LogFiles/*.log")
os.system("find Data/ModelSetup ! -name README -type f -delete")
os.system("rm *.Rout")
os.system("rm *.Rhistory")
os.system("find Data/HybridSetup ! -name README -type f -delete")
os.system("find Data/HybridPredictions ! -name README -type f -delete")
os.system("find Data/Output ! -name README -type f -delete")
os.system("find Data/SynthSetup ! -name README -type f -delete")
os.system("find Data/SynthPredictions ! -name README -type f -delete")
