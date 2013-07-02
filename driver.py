#!/usr/bin/python
import sys
import os
import re
import random
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

################### State Variables ##################

PRE_PROCESS = True
DE_EFFECT = False
SETUP_FM = True
RUN_FM = True
SETUP_HYBRID = True
RUN_HYBRID = True
POST_PROCESS = True

#--------------------------------------------------------------------



################### Pre-Process ###################
if PRE_PROCESS:
    pre.preProcess(os,utils,random,DE_EFFECT)

################### Setup Models ###################

if SETUP_FM:
    print("Setting up FM")
    modelFMSetup.FMSetup(os, utils)

################### Run Models ###################

if RUN_FM:
    print("Running FM")    
    modelFMRun.FMRun(os,utils)

################### Run Hybrid ###################

if SETUP_HYBRID:
    print("Setting up hybrid")
    hybrid.setupHybrid(os,utils)

if RUN_HYBRID:
    hybrid.runHybrid(os,utils)

################### Post Process #################

if POST_PROCESS:
    post.postProcess(os,utils)

