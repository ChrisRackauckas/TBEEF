#!/usr/bin/python
import sys
import os
import re
import random
import time
import multiprocessing as mproc
import subprocess as sproc
from math import *
WORK_PATH = os.getcwd()
sys.path.append(WORK_PATH + '/PreProcess')
sys.path.append(WORK_PATH + '/Hybrid')
sys.path.append(WORK_PATH + '/PostProcess')
sys.path.append(WORK_PATH + '/Models/libFM')
sys.path.append(WORK_PATH + '/Models/SVDFeature')
sys.path.append(WORK_PATH + '/Models')
sys.path.append(WORK_PATH + '/utils')
import Model
import runModels
import setupModels
import utils
import hybrid
import synthesize
import post
import preProcess as pre
import config
#### Holds  ####

modelList = []
testPredictionPaths = []#Array of lists of paths 
                        #where test predictions are saved
CVPredictionPaths = []  #Array of lists of paths 
                        #where CV predictions are saved
processes = []          #Array of current processes
subprocesses = []       #Array of subproccesses
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
    setupModels.setupModels(sys,os,utils,config,random,mproc,processes,modelList)

    for p in processes:
        p.join()
    processes = []
################# Run Models ###################

if config.RUN_MODELS:
    runModels.runModels(sproc,modelList,
                testPredictionPaths,CVPredictionPaths,
                config.TRIALS,subprocesses)

    #### Join #####
    
    for p in subprocesses:
        p.wait()
    subprocesses = []

    runModels.fixRun(mproc,processes,modelList)

    for p in processes:
        p.join()
    processes = []

################### Setup Hybrid ###################

modelList = []

if config.SETUP_HYBRID:
    print("Setting up hybrid")
    hybrid.setupHybrid(utils,config,random,config.BOOTSTRAP_SPLITS[1],CVPredictionPaths,testPredictionPaths,modelList,config.TRIALS)

################### Run Hybrid #####################

CVPredictionPaths = []
testPredictionPaths = []

if config.RUN_HYBRID:
    print("Running hybrid model")
    runModels.runModels(sproc,modelList,
                testPredictionPaths,CVPredictionPaths,
                config.TRIALS,subprocesses)


    for p in subprocesses:
        p.wait()
    subprocesses = []

    runModels.fixRun(mproc,processes,modelList)

    for p in processes:
        p.join()
    processes = []


################### Setup Synthesize ###################

modelList = []

if config.SETUP_SYNTHESIZE:
    print("Setting up synthesis")
    synthesize.setupSynthesize(utils,CVPredictionPaths,testPredictionPaths,config.synthModel,config.TRIALS,modelList)

################### Run Synthesize #####################

CVPredictionPaths = []
testPredictionPaths = []

if config.RUN_SYNTHESIZE:
    print("Running synthesis")
    runModels.runModels(sproc,modelList,
                testPredictionPaths,CVPredictionPaths,
                config.TRIALS,subprocesses)


    for p in subprocesses:
        p.wait()
    subprocesses = []
    
    runModels.fixRun(mproc,processes,modelList)

################### Post Process #################

if config.POST_PROCESS:
    print("Starting Post-Process") 
    post.postProcess(os,utils,config.DE_EFFECT)

################### Timer ########################

if config.TIME_RUN:
    print(time.time() - start_time,"seconds")

##################################################

print("Complete and successful!")
