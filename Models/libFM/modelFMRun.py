def FMRun(os, utils):
	for i in range(len(utils.FM_DIMS)):
		fout_temp = 'Data/ModelPredictions/temp_d'+utils.FM_DIMS[i]+'_i'+utils.FM_STR_ITER+'.txt'
		fout_final = 'Data/ModelPredictions/d'+utils.FM_DIMS[i]+'_i'+utils.FM_STR_ITER+'.txt'
		rlog = 'Data/LogFiles/d'+utils.FM_DIMS[i]+'_i'+utils.FM_STR_ITER+'.log'
		osStr = 'Models\libFM\libFM -task r -train ' + utils.FM_TRAIN_PATH + ' -test ' + utils.FM_TEST_PATH + ' -dim \''+utils.FM_GLOBAL_BIAS + ','+ utils.FM_ONE_WAY_INTERACTION + ','+ utils.FM_DIMS[i] + '\' -iter ' + utils.FM_STR_ITER + ' -rlog '+  rlog + ' -out ' + fout_temp
		print(osStr)
		os.system(osStr)
		FMFixPredictions(utils,fout_temp,fout_final)
		os.system('rm '+fout_temp)
		os.system('mv '+fout_final + ' ' + utils.FM_PREDICTIONS_PATH)


def FMFixPredictions(utils,fout_temp,fout_final):
    
    ids = open(utils.TEST_IDS_PATH, 'r') #encoding='utf-8')
    predictions = open(fout_temp, 'r') #encoding='utf-8')
    idlines = ids.readlines();
    plines = predictions.readlines();
    maxX = len(idlines)

    output = [];
    for x in range(0,maxX) :
        if x == maxX-1:
            output.append(idlines[x] + "\t" + plines[x])
        else :
            output.append(idlines[x][:-2] + "\t" + plines[x])

    outfile = open(utils.FM_PREDICTIONS_PATH, 'w') #, encoding='utf-8')

    outfile.writelines(["%s" % item  for item in output])
