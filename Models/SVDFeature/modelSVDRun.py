def SVDRun(os,utils,mproc,config,model):
    runTrain    = model[4][9]
    runCV       = model[4][10]
    runTest     = model[4][11]
    predCV      = model[4][12]
    predTest    = model[4][13]
    configPath  = model[4][16]
    predCVTmp   = predCV   + '_tmp'
    predTestTmp = predTest + '_tmp'
    bootCV      = model[4][1]
    bootTest    = model[4][2]
    print(runCV)
    print(utils.SVDFEATURE_INFER_BINARY + ' ' + configPath +
             ' test:buffer_feature=\"' + runCV + '\"' +
             ' pred=' + config.SVD_NUM_ITER + 
             ' name_pred=' + predCVTmp)   
    os.system(utils.SVDFEATURE_BINARY + ' ' + configPath +
             ' num_round=' + config.SVD_NUM_ITER) 
    os.system(utils.SVDFEATURE_INFER_BINARY + ' ' + configPath +
             ' test:buffer_feature=\"' + runCV + '\"' +
             ' pred=' + config.SVD_NUM_ITER + 
             ' name_pred=' + predCVTmp)
    os.system(utils.SVDFEATURE_INFER_BINARY + ' ' + configPath +
             ' test:buffer_feature=\"' + runTest + '\"'
             ' pred='      + config.SVD_NUM_ITER +
             ' name_pred=' + predTestTmp)
    utils.prependUserMovieToPredictions(bootCV,predCVTmp,predCV)
    utils.prependUserMovieToPredictions(bootTest,predTestTmp,predTest)
