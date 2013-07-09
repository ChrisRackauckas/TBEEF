def FMRun(os, utils,mproc,config,model):
    tag      = model[0]
    trial    = model[5]
    dim      = model[3][0]
    bootCV   = model[4][1]
    bootTest = model[4][2]
    runTrain = model[4][9]
    runCV    = model[4][10]
    runTest  = model[4][11]
    predCV   = model[4][12]
    predTest = model[4][13]
    logCV    = model[4][14]
    logTest  = model[4][15]
    fout_test_temp =  predTest  + '_temp'
    fout_cv_temp =   predCV    + '_temp'
    pTest = mproc.Process(
            target=FMInstance,
            args = (utils.LIBFM_BINARY,bootTest,  
            dim,config.FM_STR_ITER, 
            predTest,
            fout_test_temp,
            runTrain, runTest, 
            logTest, utils.FM_GLOBAL_BIAS, 
            utils.FM_ONE_WAY_INTERACTION,
            config.FM_INIT_STD,False,
            utils.prependUserMovieToPredictions))
    pCV   = mproc.Process(
            target=FMInstance,
            args = (utils.LIBFM_BINARY,bootCV,dim, 
            config.FM_STR_ITER, 
            predCV,
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

def FMInstance(libFMPath,fixIds,dim,strItr,fout_final,fout_temp,runTrain,runTest,rlog,globalBias,oneWay,initStd,printOut,prependUserMovieToPredictions):
    import os
    redirect = "> /dev/null"
    if printOut:
        redirect = ""
    os.system(libFMPath + ' -task r -train ' + 
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
