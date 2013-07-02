#!/usr/bin/python
import sys
import os
import re
from math import *
WORK_PATH = os.getcwd()
sys.path.append(WORK_PATH + '/PreProcess')
sys.path.append(WORK_PATH + '/Models/libFM')
sys.path.append(WORK_PATH + '/utils')
import modelFMRun
import modelFMSetup
import utils

################### State Variables ##################

SETUP_FM = False
RUN_FM = False

#--------------------------------------------------------------------



################### Pre-Process ###################

################### Setup Models ###################

if SETUP_FM:
    modelFMSetup.FMSetup(os, utils)

################### Run Models ###################

if RUN_FM:
    modelFMRun.FMRun(os,utils)

# Post Process





