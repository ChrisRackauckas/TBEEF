def runModels(sproc,modelList,testPredictionPaths,CVPredictionPaths,trials):
    subprocesses = []
    for trial in range(0,trials):
        # Setup utility arrays
        testPredictionPaths.append([])
        CVPredictionPaths.append([])
    for model in modelList:
        print("Running Model " + model.tag)
        model.run(sproc,subprocesses)
        testPredictionPaths[int(model.trial)].append(model.predTest)
        CVPredictionPaths[int(model.trial)].append(model.predCV)

    for p in subprocesses:
        p.wait()


def fixRun(mproc,modelList):
    processes = []
    for model in modelList:
        p = mproc.Process(target=model.fixRun)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
