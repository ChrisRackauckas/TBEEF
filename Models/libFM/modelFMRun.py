def FMRun(os, utils,mproc):
	for dim in utils.FM_DIMS:
		fout_test_final = 'Data/ModelPredictions/FM_test_d' + \
			dim +'_i'+ utils.FM_STR_ITER +'.txt'
		fout_cv_final = 'Data/ModelPredictions/FM_CV_d' +  \
			dim +'_i'+ utils.FM_STR_ITER +'.txt'

		FMTestInstance(utils,dim,utils.FM_STR_ITER, \
			  fout_test_final, \
			  utils.FM_TRAIN_PATH, \
			  utils.FM_TEST_PATH, utils.FM_GLOBAL_BIAS, \
			  utils.FM_ONE_WAY_INTERACTION)
		FMCVInstance(utils.PROCESSED_CV_PATH,dim, \
			  utils.FM_STR_ITER, \
			  fout_cv_final, \
			  utils.FM_TRAIN_PATH, \
			  utils.FM_CV_PATH, utils.FM_GLOBAL_BIAS, \
			  utils.FM_ONE_WAY_INTERACTION)
		utils.testPredictionPaths.append(fout_test_final)
		utils.CVPredictionPaths.append(fout_cv_final)

def FMTestInstance(utils,dim,strItr,fout_test_final,trainPath,testPath,globalBias,oneWay):
	import os
	fout_test_temp = 'Data/ModelPredictions/FM_test_temp_d' + \
			dim +'_i'+ strItr +'.txt'
	rlog = 'Data/LogFiles/test_d' + dim + \
		'_i'+ strItr +'.log'
	osStrTest = './Models/libFM/libFM -task r -train ' + \
		trainPath  + ' -test ' + \
		testPath + ' -dim \'' + \
		globalBias + ','+ \
		oneWay + ','+ \
		dim + '\' -iter ' + \
		strItr + ' -rlog '+  \
		rlog + ' -out ' + fout_test_temp
	os.system(osStrTest)
	utils.fixTestPredictions(utils,fout_test_temp,fout_test_final)

def FMCVInstance(processedCVPath,dim,strItr,fout_cv_final,trainPath,CVPath,globalBias,oneWay):
	import os
	fout_cv_temp = 'Data/ModelPredictions/FM_CV_temp_d' + \
			dim +'_i'+ strItr +'.txt'
	rlog = 'Data/LogFiles/test_d' + dim + \
		'_i'+ strItr +'.log'
	osStrCV = './Models/libFM/libFM -task r -train ' + \
		trainPath + ' -test ' + \
		CVPath + ' -dim \'' + \
		globalBias + ','+ \
		oneWay + ','+ \
		dim + '\' -iter ' + \
		strItr + ' -rlog '+  \
		rlog + ' -out ' + fout_cv_temp
	os.system(osStrCV)
	FMFixCV(processedCVPath,fout_cv_temp,fout_cv_final)

def FMFixCV(processedCVPath,fout_temp,fout_final):
    ids = open(processedCVPath, 'r')
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
