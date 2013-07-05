def FMRunParallel(os, utils,mproc):
    for dim in utils.FM_DIMS:
        fout_test_final = 'Data/ModelPredictions/FM_test_d' + \
            dim +'_i'+ utils.FM_STR_ITER +'.txt'
        fout_cv_final = 'Data/ModelPredictions/FM_CV_d' +  \
            dim +'_i'+ utils.FM_STR_ITER +'.txt'
        pTest = mproc.Process(
              target=FMTestInstance,
              args = (utils.TEST_IDS_PATH,  
                dim,utils.FM_STR_ITER, 
                fout_test_final, 
                utils.FM_TRAIN_PATH, 
                utils.FM_TEST_PATH, utils.FM_GLOBAL_BIAS, 
                utils.FM_ONE_WAY_INTERACTION))
        pCV   = mproc.Process(
              target=FMCVInstance,
              args = (utils.PROCESSED_CV_PATH,dim, 
                utils.FM_STR_ITER, 
                fout_cv_final, 
                utils.FM_TRAIN_PATH, 
                utils.FM_CV_PATH, utils.FM_GLOBAL_BIAS, 
                utils.FM_ONE_WAY_INTERACTION))
        utils.processes.append(pTest)
        utils.processes.append(pCV)
        pTest.start()
        pCV.start()
        utils.testPredictionPaths.append(fout_test_final)
        utils.CVPredictionPaths.append(fout_cv_final)

def FMRunSerial(os,utils):
    for dim in utils.FM_DIMS:
        fout_test_final = 'Data/ModelPredictions/FM_test_d' + \
            dim +'_i'+ utils.FM_STR_ITER +'.txt'
        fout_cv_final = 'Data/ModelPredictions/FM_CV_d' +  \
            dim +'_i'+ utils.FM_STR_ITER +'.txt'
        FMTestInstance(utils.TEST_IDS_PATH,dim,utils.FM_STR_ITER, 
                fout_test_final, 
                utils.FM_TRAIN_PATH, 
                utils.FM_TEST_PATH, utils.FM_GLOBAL_BIAS, 
                utils.FM_ONE_WAY_INTERACTION)
        FMCVInstance(utils.PROCESSED_CV_PATH,dim, 
                utils.FM_STR_ITER, 
                fout_cv_final, 
                utils.FM_TRAIN_PATH, 
                utils.FM_CV_PATH, utils.FM_GLOBAL_BIAS, 
                utils.FM_ONE_WAY_INTERACTION)
        utils.testPredictionPaths.append(fout_test_final)
        utils.CVPredictionPaths.append(fout_cv_final)

def FMTestInstance(idsPath,dim,strItr,fout_test_final,trainPath,testPath,globalBias,oneWay):
    import os
    import utils
    fout_test_temp = 'Data/ModelPredictions/FM_test_temp_d' + \
            dim +'_i'+ strItr +'.txt'
    rlog = 'Data/LogFiles/test_d' + dim + \
        '_i'+ strItr +'.log'
    os.system('./Models/libFM/libFM -task r -train ' + 
        trainPath  + ' -test ' + 
        testPath + ' -dim \'' + 
        globalBias + ','+ 
        oneWay + ','+ 
        dim + '\' -iter ' + 
        strItr + ' -rlog '+  
        rlog + ' -out ' + 
        fout_test_temp + '> /dev/null')
    utils.fixTestPredictions(idsPath,fout_test_temp,fout_test_final)

def FMCVInstance(processedCVPath,dim,strItr,fout_cv_final,trainPath,CVPath,globalBias,oneWay):
    import os
    fout_cv_temp = 'Data/ModelPredictions/FM_CV_temp_d' + \
            dim +'_i'+ strItr +'.txt'
    rlog = 'Data/LogFiles/test_d' + dim + \
        '_i'+ strItr +'.log'
    os.system('./Models/libFM/libFM -task r -train ' + 
        trainPath + ' -test ' + 
        CVPath + ' -dim \'' + 
        globalBias + ','+ 
        oneWay + ','+ 
        dim + '\' -iter ' + 
        strItr + ' -rlog '+  
        rlog + ' -out ' + 
        fout_cv_temp + '> /dev/null')
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
