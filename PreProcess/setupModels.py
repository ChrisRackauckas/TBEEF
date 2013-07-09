def setupModels(sys,os,utils,config,random,mproc,processes,modelList):
    from FMModel import FMModel
    from SVDModel import SVDModel
    for trial in range(0,config.TRIALS):
        strTrial = str(trial)
        print("Setting up trial " + strTrial)
        ### Setup boot strings ###
        bootTrain =  utils.MODEL_BOOT_PATH  +   \
                                   '_train' + '_t' + strTrial
        bootCV    =  utils.MODEL_BOOT_PATH  +   \
                                      '_CV' + '_t' + strTrial
        bootTest  =  utils.MODEL_BOOT_PATH + \
                        '_test' + '_t' + strTrial 
        ### Split dataset ###
        ### Setup test datasets separate for parallel ###
        utils.bootsplit(utils.PROCESSED_DATA_PATH,
                utils.PROCESSED_DATA_PATH_TEMP + '_t' + strTrial,
                bootTrain, bootCV, config.BOOTSTRAP_SPLITS[0],
                random)
        os.system('cp ' + utils.TEST_IDS_DUMMY_PATH +
                    ' ' + bootTest)

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
