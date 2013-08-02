### Cleans the data folder out ###
### Takes an argument, 1 to delete PreProcess folder items ###
### Defaults to 0 ###

import os
import sys
WORK_PATH = os.getcwd()
try:
    delPre = int(sys.argv[1]) == 1
except IndexError:
    delPre = False

os.system("find Data/Effects ! -name README -type f -delete")
if delPre:
    os.system("find Data/PreProcessed ! -name README -type f -delete")
os.system("find Data/ModelPredictions ! -name README -type f -delete")
os.system("find Data/ModelData/* -maxdepth 0 -name 'README' -prune -o -exec rm -rf '{}' ';'")
os.system("find Data/LogFiles ! -name README -type f -delete")
os.system("find Data/ModelSetup ! -name README -type f -delete")
os.system("rm *.Rout")
os.system("rm *.Rhistory")
os.system("rm TBEEF.*")
os.system("find Data/HybridSetup ! -name README -type f -delete")
os.system("find Data/HybridPredictions ! -name README -type f -delete")
os.system("find Data/Output ! -name README -type f -delete")
os.system("find Data/SynthSetup ! -name README -type f -delete")
os.system("find Data/SynthPredictions ! -name README -type f -delete")
