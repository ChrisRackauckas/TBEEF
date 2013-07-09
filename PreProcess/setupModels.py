def setupModels(sys,os,utils,config,random,mproc):
    import modelFMSetup
    import modelSVDSetup
    for trial in range(0,config.TRIALS):
        strTrial = str(trial)
        ### Bootsplit the dataset ###
        bootTrain =  utils.MODEL_BOOT_PATH  +   \
                                   '_train' + '_t' + strTrial
        bootCV    =  utils.MODEL_BOOT_PATH  +   \
                                      '_CV' + '_t' + strTrial
        utils.bootsplit(utils.PROCESSED_DATA_PATH,
                utils.PROCESSED_DATA_PATH_TEMP + '_t' + strTrial,
                bootTrain, bootCV, config.BOOTSTRAP_SPLITS[0],
                random)
        
        for model in config.models:
            tag = model[0]
            ### Define paths and append to modelsData ###
            bootTest  =  utils.MODEL_BOOT_PATH     + tag + \
                                    '_test' + '_t' + strTrial     
            featTrain  = utils.MODEL_FEATURED_PATH + tag + \
                                   '_train' + '_t' + strTrial
            featCV     = utils.MODEL_FEATURED_PATH + tag + \
                                      '_CV' + '_t' + strTrial
            featTest   = utils.MODEL_FEATURED_PATH + tag + \
                                    '_test' + '_t' + strTrial
            tmpTrain   = utils.MODEL_TMP_PATH      + tag + \
                                   '_train' + '_t' + strTrial
            tmpCV      = utils.MODEL_TMP_PATH      + tag + \
                                      '_CV' + '_t' + strTrial
            tmpTest    = utils.MODEL_TMP_PATH      + tag + \
                                     '_test'+ '_t' + strTrial 
            runTrain   = utils.MODEL_RUN_PATH      + tag + \
                                   '_train' + '_t' + strTrial
            runCV      = utils.MODEL_RUN_PATH      + tag + \
                                      '_CV' + '_t' + strTrial
            runTest    = utils.MODEL_RUN_PATH      + tag + \
                                    '_test' + '_t' + strTrial
            predCV     = utils.MODEL_PREDICT_PATH  + tag + \
                                       '_CV'+ '_t' + strTrial
            predTest   = utils.MODEL_PREDICT_PATH  + tag + \
                                    '_test' + '_t' + strTrial
            logCV      = utils.MODEL_LOG_PATH      + tag + \
                                      '_CV' + '_t' + strTrial
            logTest    = utils.MODEL_LOG_PATH      + tag + \
                                    '_test' + '_t' + strTrial
            configCV   = utils.MODEL_CONFIG_PATH   + tag + \
                                      '_CV' + '_t' + strTrial
            configTest = utils.MODEL_CONFIG_PATH   + tag + \
                                    '_test' + '_t' + strTrial
            modelPaths = [bootTrain,bootCV,bootTest,
                          featTrain,featCV,featTest,
                          tmpTrain,tmpCV,tmpTest,
                          runTrain,runCV,runTest,
                          predCV,predTest,logCV,
                          logTest,configCV,configTest]
            modelData = [tag,model[1],model[2],model[3],modelPaths,strTrial]
            utils.modelsData.append(modelData)

            ### Setup test datasets separate for parallel ###
            if modelData[1] == 'FM':
                os.system('cp ' + utils.TEST_IDS_DUMMY_PATH +
                    ' ' + bootTest)
            else :
                os.system('cp ' + utils.TEST_IDS_PATH +
                    ' ' + bootTest)

            ### Run Setup Functions
            if model[1] == 'FM':
                modelFMSetup.FMSetup(os,utils,modelData)
            if model[1] == 'SVD':
                modelSVDSetup.SVDSetup(os,utils,modelData,config)
