def FMRun(os, utils,mproc,config,model):
    tag = model[0]
    dim= model[3][0]
    bootCV   = model[4][1]
    bootTest = model[4][2]
    runTrain = model[4][9]
    runCV    = model[4][10]
    runTest  = model[4][11]
    predCV   = model[4][12]
    predTest = model[4][13]
    logCV    = model[4][14]
    logTest  = model[4][15]
    fout_test_final = predTest + '_d' + \
            dim +'_i'+ config.FM_STR_ITER +'.txt'
    fout_cv_final = predCV +'_d' +  \
            dim +'_i'+ config.FM_STR_ITER +'.txt'
    fout_test_temp = predTest + '_temp__d' + \
            dim +'_i'+ config.FM_STR_ITER +'.txt'
    fout_cv_temp = predCV +'_temp_d' +  \
            dim +'_i'+ config.FM_STR_ITER +'.txt'
    pTest = mproc.Process(
            target=FMInstance,
            args = (bootTest,  
            dim,config.FM_STR_ITER, 
            fout_test_final,
            fout_test_temp,
            runTrain, runTest, 
            logTest, utils.FM_GLOBAL_BIAS, 
            utils.FM_ONE_WAY_INTERACTION,
            config.FM_INIT_STD,False,
            utils.prependUserMovieToPredictions))
    pCV   = mproc.Process(
            target=FMInstance,
            args = (bootCV,dim, 
            config.FM_STR_ITER, 
            fout_cv_final,
            fout_cv_temp,
            runTrain, runCV, 
            logCV, utils.FM_GLOBAL_BIAS, 
            utils.FM_ONE_WAY_INTERACTION,
            config.FM_INIT_STD,True,
            utils.prependUserMovieToPredictions))
    utils.processes.append(pTest)
    utils.processes.append(pCV)
    pTest.start()
    pCV.start()
    utils.testPredictionPaths.append(fout_test_final)
    utils.CVPredictionPaths.append(fout_cv_final)

def FMInstance(fixIds,dim,strItr,fout_final,fout_temp,runTrain,runTest,logTest,globalBias,oneWay,initStd,printOut,prependUserMovieToPredictions):
    import os
    redirect = "> /dev/null"
    if printOut:
        redirect = ""
    rlog = 'Data/LogFiles/test_d' + dim + \
        '_i'+ strItr +'.log'
    os.system('./Models/libFM/libFM -task r -train ' + 
        runTrain + ' -test ' + 
        runTest + ' -init_stdev ' + 
        initStd + ' -dim \'' + 
        globalBias + ','+ 
        oneWay + ','+ 
        dim + '\' -iter ' + 
        strItr + ' -rlog '+  
        rlog + ' -out ' + 
        fout_temp + redirect)
    prependUserMovieToPredictions(fixIds,fout_temp,fout_final)
