def setupModels(sys,os,utils,config,random,mproc,modelList):
    processes = []
    from FMModel import FMModel
    from SVDModel import SVDModel
    for trial in range(0,config.TRIALS):
        strTrial = str(trial)
        print("Setting up trial " + strTrial)
        p = mproc.Process(target=setupTrial,
                args=(utils.MODEL_BOOT_PATH,
                    strTrial,
                    utils.PROCESSED_DATA_PATH,
                    utils.PROCESSED_DATA_PATH_TEMP,
                    utils.bootsplit,
                    config.BOOTSTRAP_SPLITS[0],
                    random, utils.TEST_IDS_DUMMY_PATH))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
    processes = []

    for trial in range(0,config.TRIALS):
        strTrial = str(trial)
        for configModel in config.models:
            print("Setting up model " + configModel[0])
            if configModel[1] == 'FM':
                model = FMModel(configModel,utils,config,strTrial)
            if configModel[1] == 'SVD':
                model = SVDModel(configModel,utils,config,strTrial)
            p = mproc.Process(target=model.setup)
            processes.append(p)
            p.start()
            modelList.append(model)
    
    for p in processes:
        p.join()

def setupTrial(modelBootPath,strTrial,processedDataPath,processedDataPathTemp,bootsplitFunc,split,random,testIdsDummyPath):
    import os
    ### Setup boot strings ###
    bootTrain =  modelBootPath  +   \
                 'train' + '_t' + strTrial
    bootCV    =  modelBootPath  +   \
                 'CV' + '_t' + strTrial
    bootTest  =  modelBootPath  + \
                 'test' + '_t' + strTrial 
    ### Split dataset ###
    ### Setup test datasets separate for parallel ###
    bootsplitFunc(processedDataPath,
                processedDataPathTemp + '_t' + strTrial,
                bootTrain, bootCV, split,
                random)
    os.system('cp ' + testIdsDummyPath +
                    ' ' + bootTest)
