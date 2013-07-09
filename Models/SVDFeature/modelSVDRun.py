def SVDRun(os,utils,mproc,config,model):
    runTrain  = model[4][9]
    runCV     = model[4][10]
    runTest   = model[4][11]
    predCV    = model[4][12]
    predTest  = model[4][13]
    configPath= model[4][16]
    os.system(utils.SVDFEATURE_BINARY + ' ' + configPath +
             ' num_round=' + config.SVD_NUM_ITER) 
    os.system(utils.SVDFEATURE_INFER_BINARY + ' ' + configPath +
             ' pred=' + config.SVD_NUM_ITER + 
             ' name_pred=' + predCV)
    os.system(utils.SVDFEATURE_INFER_BINARY + ' ' + configPath +
             ' pred='      + config.SVD_NUM_ITER +
             ' name_pred=' + predTest)
