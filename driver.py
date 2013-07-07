#!/usr/bin/python
import sys
import os
import re
from random import random
import time
import multiprocessing as mproc
from math import *
WORK_PATH = os.getcwd()
sys.path.append(WORK_PATH + '/PreProcess')
sys.path.append(WORK_PATH + '/PostProcess')
sys.path.append(WORK_PATH + '/Models/libFM')
sys.path.append(WORK_PATH + '/utils')
import modelFMRun
import featureSetupFM as feat
import modelFMSetup
#import modelRRSetup
import utils
import hybrid
import post
import preProcess as pre
import config
#--------------------------------------------------------------------

################## Timer ##########################
if config.TIME_RUN:
        print("Start Timing Parallel")
        start_time = time.time()

################### Pre-Process ###################
if config.PRE_PROCESS:
    print("Pre-Processing")
    pre.preProcess(os,utils,random,config.DE_EFFECT, config.RANDOMIZE_DATA)
    print("Pre-Processing Complete")

################### Add Features ###################

if config.FEATURES:
    feat.createFeature(os,utils,config.MOVIE_TAG, \
                       config.SOCIAL,config.HISTORY)

################### Setup Models ###################

if config.RUN_PARALLEL:
    if config.SETUP_FM:
        print("Setting up FM")
        p = mproc.Process(
                target = modelFMSetup.FMSetup,
                args=(os,utils)) 

        p.start()
        utils.processes.append(p)
    ####Join #####
    for p in utils.processes:
        p.join()
    utils.processes = []

if config.RUN_SERIAL:
    if config.SETUP_FM:
        print("Setting up FM")
        modelFMSetup.FMSetup(os,utils) 

################## Run Models ###################

#Parallel--------------------------------
if config.RUN_PARALLEL:
    if config.RUN_FM:
        print("Running FM")
        modelFMRun.FMRunParallel(os,utils, mproc,config)
    
####Join #####
    
        for p in utils.processes:
            p.join()
        utils.prcesses = []
#Serial------------------------------------

if config.RUN_SERIAL:
    if config.TIME_RUN:
        print("Start timing serial")
        start_time = time.time()

    if config.RUN_FM:
        print("Running FM")    
        modelFMRun.FMRunSerial(os,utils,config)

################### Run Hybrid ###################

if config.SETUP_HYBRID:
    print("Setting up hybrid")
    hybrid.setupHybrid(os,utils)

if config.RUN_HYBRID:
    print("Running hybrid model")
    hybrid.runHybrid(os,utils,config.HYBRID_CHOICE,config.RR_CONST)

################### Post Process #################

if config.POST_PROCESS:
    print("Starting Post-Process") 
    post.postProcess(os,utils, config.DE_EFFECT)

################### Timer ########################

    if config.TIME_RUN:
        print(time.time() - start_time,"seconds")

##################################################

print("Complete and successful!")
