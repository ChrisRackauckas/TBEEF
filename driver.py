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

SETUP_FM = True
RUN_FM = True
SETUP_HYBRID = True
RUN_HYBRID = True
POST_PROCESS = True

#--------------------------------------------------------------------



################### Pre-Process ###################
pre.preProcess(os,utils,random)

################### Setup Models ###################

if SETUP_FM:
    modelFMSetup.FMSetup(os, utils)

################### Run Models ###################

if RUN_FM:
    modelFMRun.FMRun(os,utils)

################### Run Hybrid ###################

if SETUP_HYBRID:
    hybrid.setupHybrid(os,utils)

if RUN_HYBRID:
    hybrid.runHybrid(os,utils)

################### Post Process #################

if POST_PROCESS:
    post.postProcess(os,utils)

