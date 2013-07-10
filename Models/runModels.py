def runModels(sproc,modelList,testPredictionPaths,CVPredictionPaths,trials,subprocesses):
    for trial in range(0,trials):
        # Setup utility arrays
        testPredictionPaths.append([])
        CVPredictionPaths.append([])
    for model in modelList:
        print("Running Model " + model.tag)
        model.run(sproc,subprocesses)
        testPredictionPaths[int(model.trial)].append(model.predCV)
        CVPredictionPaths[int(model.trial)].append(model.predTest)

def fixRun(mproc,processes,modelList):
    for model in modelList:
        p = mproc.Process(target=model.fixRun)
        p.start()
        processes.append(p)
