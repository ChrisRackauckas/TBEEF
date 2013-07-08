def setupModels(sys,os,utils,config,random,mproc):
    import modelFMSetup
    for model in config.models:
        
        tag = model[0]
        
        ### Define paths and append to model ###

        bootTrain = utils.MODEL_BOOT_PATH       + tag + '_train'
        bootCV    = utils.MODEL_BOOT_PATH       + tag + '_CV'
        bootTest  = utils.MODEL_BOOT_PATH       + tag + '_test'
        featTrain = utils.MODEL_FEATURED_PATH   + tag + '_train'
        featCV    = utils.MODEL_FEATURED_PATH   + tag + '_CV'
        featTest  = utils.MODEL_FEATURED_PATH   + tag + '_test'
        binTrain  = utils.MODEL_BIN_PATH        + tag + '_train'
        binCV     = utils.MODEL_BIN_PATH        + tag + '_CV'
        binTest   = utils.MODEL_BIN_PATH        + tag + '_test'
        runTrain  = utils.MODEL_RUN_PATH        + tag + '_train'
        runCV     = utils.MODEL_RUN_PATH        + tag + '_CV'
        runTest   = utils.MODEL_RUN_PATH        + tag + '_test'
        predCV    = utils.MODEL_PREDICT_PATH    + tag + '_CV'
        predTest  = utils.MODEL_PREDICT_PATH    + tag + '_test'
        logCV     = utils.MODEL_LOG_PATH        + tag + '_CV'
        logTest   = utils.MODEL_LOG_PATH        + tag + '_test'

        modelPaths = [bootTrain,bootCV,bootTest,
                      featTrain,featCV,featTest,
                      binTrain,binCV,binTest,
                      runTrain,runCV,runTest,
                      predCV,predTest,logCV,logTest]
        
        model.append(modelPaths)


        ### Bootstrap the dataset ###
        
        utils.bootstrap(utils.PROCESSED_DATA_PATH,
                bootTrain,
                config.BOOTSTRAP_SIZE_TRAIN,random)
        utils.bootstrap(utils.PROCESSED_DATA_PATH,
                bootCV,
                config.BOOTSTRAP_SIZE_CV,random)
        
        ### Setup test datasets separate for parallel ###
        
        if model[1] == 'FM':
            os.system('cp ' + utils.TEST_IDS_DUMMY_PATH +
                    ' ' + bootTest)
        else :
            os.system('cp ' + utils.TEST_IDS_PATH +
                    ' ' + bootTest)

        ### Run Setup Functions
        
        if model[1] == 'FM':
            modelFMSetup.FMSetup(os,utils,model)
        if model[1] == 'SVDFeature':
            print("SVDFeature not setup!")
