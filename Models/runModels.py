def runModels(sys,os,utils,mproc,config):
    for trial in range(0,config.TRIALS):
        utils.testPredictionPaths.append([])
        utils.CVPredictionPaths.append([])
    import modelFMRun
    for model in utils.modelsData:
        if model[1] == 'FM':
            modelFMRun.FMRun(os,utils,mproc,config,model)
        if model[2] == 'SVDFeature':
            print("Sorry, not implemented yet")
        utils.testPredictionPaths[model[5]].append(model[4][13])
        utils.CVPredictionPaths[model[5]].append(model[4][12])
