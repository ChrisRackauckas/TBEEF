#!/usr/bin/python
import sys
import os
import re
import random
import time
import multiprocessing as mproc
from math import *
WORK_PATH = os.getcwd()
sys.path.append(WORK_PATH + '/PreProcess')
sys.path.append(WORK_PATH + '/Hybrid')
sys.path.append(WORK_PATH + '/PostProcess')
sys.path.append(WORK_PATH + '/Models/libFM')
sys.path.append(WORK_PATH + '/Models')
sys.path.append(WORK_PATH + '/utils')
sys.path.append(WORK_PATH + '/PreProcess/libFM')
sys.path.append(WORK_PATH + '/PreProcess/svdFeature')
import runModels
import setupModels
import utils
import hybrid
import post
import preProcess as pre
import config

#--------------------------------------------------------------------

################## Timer ##########################

if config.TIME_RUN:
        print("Start Timing")
        start_time = time.time()

################### Pre-Process ###################

if config.PRE_PROCESS:
    print("Pre-Processing")
    pre.preProcess(os,utils,random,config.DE_EFFECT)
    print("Pre-Processing Complete")

################### Setup Models ###################

if config.SETUP_MODELS:
    setupModels.setupModels(sys,os,utils,config,random,mproc)

    #### Join #####

    for p in utils.processes:
        p.join()
    utils.processes = []

################# Run Models ###################

if config.RUN_MODELS:
    runModels.runModels(sys,os,utils,mproc,config)

    #### Join #####
    
    for p in utils.processes:
        p.join()
    utils.prcesses = []

################### Setup Hybrid ###################

if config.SETUP_HYBRID:
    print("Setting up hybrid")
    hybrid.setupHybrid(os,utils)

################### Run Hybrid #####################

if config.RUN_HYBRID:
    print("Running hybrid model")
    hybrid.runHybrid(os,utils,config,mproc)

################### Post Process #################

if config.POST_PROCESS:
    print("Starting Post-Process") 
    post.postProcess(os,utils,config.DE_EFFECT)

################### Timer ########################

if config.TIME_RUN:
    print(time.time() - start_time,"seconds")

##################################################

print("Complete and successful!")
