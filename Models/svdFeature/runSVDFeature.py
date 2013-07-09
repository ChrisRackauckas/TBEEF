def runSVDFeature(os,utils,mproc,config,model):
	itr = model[3][1]
    runTrain = model[4][9]
    runCV    = model[4][10]
    runTest  = model[4][11]
    predCV   = model[4][12]
    predTest = model[4][13]
	os.system(utils.SVDFEATURE_BINARY + ' ' + 
