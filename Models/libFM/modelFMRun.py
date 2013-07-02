def FMRun(os, utils):
	for i in range(len(utils.FM_DIMS)):
		fout_test_temp = 'Data/ModelPredictions/FM_test_temp_d'+utils.FM_DIMS[i]+'_i'+utils.FM_STR_ITER+'.txt'
		fout_test_final = 'Data/ModelPredictions/FM_test_d'+utils.FM_DIMS[i]+'_i'+utils.FM_STR_ITER+'.txt'
		fout_cv_temp = 'Data/ModelPredictions/FM_CV_temp_d'+utils.FM_DIMS[i]+'_i'+utils.FM_STR_ITER+'.txt'
		fout_cv_final = 'Data/ModelPredictions/FM_CV_d'+utils.FM_DIMS[i]+'_i'+utils.FM_STR_ITER+'.txt'
		rlog = 'Data/LogFiles/d'+utils.FM_DIMS[i]+'_i'+utils.FM_STR_ITER+'.log'
		osStrTest = './Models/libFM/libFM -task r -train ' + utils.FM_TRAIN_PATH + ' -test ' + utils.FM_TEST_PATH + ' -dim \''+utils.FM_GLOBAL_BIAS + ','+ utils.FM_ONE_WAY_INTERACTION + ','+ utils.FM_DIMS[i] + '\' -iter ' + utils.FM_STR_ITER + ' -rlog '+  rlog + ' -out ' + fout_test_temp
		osStrCV = './Models/libFM/libFM -task r -train ' + utils.FM_TRAIN_PATH + ' -test ' + utils.FM_CV_PATH + ' -dim \''+utils.FM_GLOBAL_BIAS + ','+ utils.FM_ONE_WAY_INTERACTION + ','+ utils.FM_DIMS[i] + '\' -iter ' + utils.FM_STR_ITER + ' -rlog '+  rlog + ' -out ' + fout_cv_temp
		os.system(osStrTest)
		os.system(osStrCV)
		utils.fixTestPredictions(utils,fout_test_temp,fout_test_final)
		FMFixCV(utils,fout_cv_temp,fout_cv_final)
		os.system('rm '+fout_test_temp)
		os.system('rm '+fout_cv_temp)
		utils.testPredictionPaths.append(fout_test_final)
		utils.CVPredictionPaths.append(fout_cv_final)


def FMFixCV(utils,fout_temp,fout_final):
    ids = open(utils.PROCESSED_CV_PATH, 'r')
    predictions = open(fout_temp, 'r')
    idlines = ids.readlines();
    plines = predictions.readlines();
    maxX = len(idlines)

    output = [];
    for x in range(0,maxX) :
        if x == maxX:
            output.append(idlines[x:-5] + "\t" + plines[x])
        else :
            output.append(idlines[x][:-7] + "\t" + plines[x])
    outfile = open(fout_final, 'w')
    outfile.writelines(["%s" % item  for item in output])
