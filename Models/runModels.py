def runModels(sys,os,utils,mproc,config):
    import modelFMRun
    import modelSVDRun
    for trial in range(0,config.TRIALS):
        # Setup utility arrays
        utils.testPredictionPaths.append([])
        utils.CVPredictionPaths.append([])
    for model in utils.modelsData:
        print("Running Model " + model[0])
        if model[1] == 'FM':
            modelFMRun.FMRun(os,utils,mproc,config,model)
        if model[1] == 'SVD':
            modelSVDRun.SVDRun(os,utils,mproc,config,model)
        utils.testPredictionPaths[int(model[5])].append(model[4][13])
        utils.CVPredictionPaths[int(model[5])].append(model[4][12])
