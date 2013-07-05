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
sys.path.append(WORK_PATH + '/PostProcess')
sys.path.append(WORK_PATH + '/Models/libFM')
sys.path.append(WORK_PATH + '/utils')
import modelFMRun
import modelFMSetup
import utils
import hybrid
import post
import preProcess as pre

################### Select Parts  ##################

PRE_PROCESS  = True
DE_EFFECT    = True
SETUP_FM     = True
RUN_FM       = True
SETUP_HYBRID = True
RUN_HYBRID   = True
POST_PROCESS = True

################## Select Performance ##############

RUN_PARALLEL = True
RUN_SERIAL   = False
TIME_RUN     = False

#--------------------------------------------------------------------



################### Pre-Process ###################
if PRE_PROCESS:
    print("Pre-Processing")
    pre.preProcess(os,utils,random,DE_EFFECT)
    print("Pre-Processing Complete")

################### Setup Models ###################

if SETUP_FM:
    print("Setting up FM")
    modelFMSetup.FMSetup(os, utils)

################### Run Models ###################

#Parallel--------------------------------
if RUN_PARALLEL:
    if TIME_RUN:
        print("Start timing parallel")
        start_time = time.time()

    if RUN_FM:
        print("Running FM")
        modelFMRun.FMRunParallel(os,utils, mproc)
    
####Join #####
    
        for p in utils.processes:
            p.join()

    if TIME_RUN:
        print(time.time() - start_time,"seconds")

################## Serial #######################

if RUN_SERIAL:
    if TIME_RUN:
        print("Start timing serial")
        start_time = time.time()

    if RUN_FM:
        print("Running FM")    
        modelFMRun.FMRunSerial(os,utils)
    
    if TIME_RUN:
        print(time.time() - start_time,"seconds")




################### Run Hybrid ###################

if SETUP_HYBRID:
    print("Setting up hybrid")
    hybrid.setupHybrid(os,utils)

if RUN_HYBRID:
    print("Running hybrid model")
    hybrid.runHybrid(os,utils)

################### Post Process #################

if POST_PROCESS:
    print("Starting Post-Process") 
    post.postProcess(os,utils, DE_EFFECT)

print("Complete and successful!")
