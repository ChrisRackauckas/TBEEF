def runSVDFeature(os,utils,mproc,config,model):
	itr = model[3][1]
    runTrain  = model[4][9]
    runCV     = model[4][10]
    runTest   = model[4][11]
    predCV    = model[4][12]
    predTest  = model[4][13]
    configCV  = model[4][15]
    configTest= model[4][16]
	os.system(utils.SVDFEATURE_BINARY + ' ' + configCV +
             'num_round=' + config.SVDFEATURE_NUM_ITER)
    os.system(utils.SVDFEATURE_INFER_BINARY + ' ' + configCV +
             'pred=' + config.SVDFEATURE_NUM_ITER + 
             'name_pred=' + predCV)
    os.system(utils.SVDFEATURE_INFER_BINARY + ' ' + configCV +
             'pred='      + config.SVDFEATURE_NUM_ITER +
             'name_pred=' + predTest)
