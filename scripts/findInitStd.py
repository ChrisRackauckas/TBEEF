#!/user/bin/python

### This script uses a small amount of iterations
### on many different initial stdevs
### in order to find which one converges the fastest

import sys
import os
from math import *
os.chdir('../')
WORK_PATH = os.getcwd()
sys.path.append(WORK_PATH + '/utils')
sys.path.append(WORK_PATH + '/Models/libFM')
import modelFMRun
import utils
printOut = True

iters = "20"
simDim = "8"
initStds = [ round(x * 0.05, 1) for x in range(0, 12)]

for i in initStds:
    iStr = str(i)
    print("initStd is " + iStr)
    modelFMRun.FMCVInstance(utils.PROCESSED_CV_PATH,simDim, 
                iters, 
                'tmp.txt', 
                utils.FM_TRAIN_PATH, 
                utils.FM_CV_PATH, utils.FM_GLOBAL_BIAS, 
                utils.FM_ONE_WAY_INTERACTION,
                printOut,
                iStr,False)    
