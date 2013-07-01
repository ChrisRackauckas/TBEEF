#!/usr/bin/python
import os
import re
from math import *

#--------------------------------------------------------------------

work_path = '/Users/jarviscolin/Desktop/work/libfm-1.34.src'

template = 'bin/libFM -task r -train training_set_nodups.libfm -test predict_dummy.libfm -dim ’1,1,8’ -out colin_test8.txt'


dim  = [ '1', '2', '3', '4', '5', '6', '7', '8' ]


GLOBAL_BIAS = '1' #either 1 or 0
ONE_WAY_INTERACTION = '1' #either 1 or 0
ITER = 1000
STR_ITER = str(ITER)

SAVE_PATH = 'iter_'+STR_ITER
os.system('mkdir '+SAVE_PATH) #new folder 

#fix prediction files (makes three column files)

def fixPredictions(predictionsStr, outputStr):
    id_path = '../data/predict.txt'
    ids = open(id_path, 'r') #encoding='utf-8')
    predictions = open(predictionsStr, 'r') #encoding='utf-8')
    
    idlines = ids.readlines();
    plines = predictions.readlines();
    maxX = len(idlines)

    output = [];
    for x in range(0,maxX) :
        if x == maxX-1:
            output.append(idlines[x] + "\t" + plines[x])
        else :
            output.append(idlines[x][:-2] + "\t" + plines[x])

    outfile = open(outputStr, 'w') #, encoding='utf-8')

    outfile.writelines(["%s" % item  for item in output])



# generate predictions
for i in range(len(dim)):
    fout_temp = 'temp_d'+dim[i]+'_i'+STR_ITER+'.txt'
    fout_final = 'd'+dim[i]+'_i'+STR_ITER+'.txt'
    rlog = 'd'+dim[i]+'_i'+STR_ITER+'.log'
    
    os.system('bin/libFM -task r -train training_set_nodups.libfm -test predict_dummy.libfm \
                  -dim ’'+GLOBAL_BIAS +','+ ONE_WAY_INTERACTION +','+ dim[i] +'’ -iter '+ STR_ITER \
                  + ' -rlog '+  rlog +' -out '+ fout_temp)  

    fixPredictions(fout_temp, fout_final)
    os.system('rm '+fout_temp)
    os.system('mv '+fout_final+' '+ rlog +' '+ SAVE_PATH)



