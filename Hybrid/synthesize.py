import hybrid
from SynthModel import SynthModel
def setupSynthesize(utils,CVPredictionPaths,testPredictionPaths,split,random,configModel,trials,modelList,mproc,processes):
    processes = []
    for trial in range(0,trials):
        strTrial = str(trial)
        p = mproc.Process(target=synthSetupTrial,
                        args=(utils.SYNTH_ORIGINAL_PATH,strTrial,
                        utils.HYBRID_BOOT_PATH,
                        utils.SYNTH_BOOT_PATH,
                        CVPredictionPaths[trial],
                        testPredictionPaths[trial],
                        split,random,
                        utils.bootsplit,
                        utils.grabCSVColumn,
                        hybrid.buildTrainingMatrixFromPredictions,
                        hybrid.buildPredictorMatrixFromPredictions,
                        hybrid.addHeader))
        p.start()
        processes.append(p)
        synthModel = SynthModel(configModel,utils,strTrial)
        modelList.append(synthModel)  

    for p in processes:
        p.join()
        
        
def synthSetupTrial(synthOriginalPath,strTrial,hybridBootPath,synthBootPath,CVPredictionPaths,testPredictionPaths,split,random,bootsplitFunc,grabCSVColumnFunc,buildTrainingMatrixFromPredictionsFunc,buildPredictorMatrixFromPredictionsFunc,addHeaderFunc):
        synthOriginal = synthOriginalPath \
                    + 'train_t' + strTrial
        synthPredict  = synthOriginalPath \
                    + 'test_t'  + strTrial
        bootCV = hybridBootPath + 'CV_t' + strTrial + '_tmp'
        buildTrainingMatrixFromPredictionsFunc(bootCV,synthOriginal,
                    CVPredictionPaths,grabCSVColumnFunc,0)
        buildPredictorMatrixFromPredictionsFunc(testPredictionPaths,
                    grabCSVColumnFunc,synthPredict + '_tmp')
        bootsplitFunc(synthOriginal,synthOriginal + '_tmp',
                      synthBootPath + 'train_t' + strTrial + '_tmp',
                      synthBootPath + 'CV_t'    + strTrial + '_tmp',
                      split,random)
        addHeaderFunc(synthBootPath + 'train_t' + strTrial + '_tmp',
                      synthBootPath + 'train_t' + strTrial ,False)
        addHeaderFunc(synthBootPath + 'CV_t'    + strTrial + '_tmp',
                      synthBootPath + 'CV_t'    + strTrial ,False)
        addHeaderFunc(synthPredict + '_tmp', synthPredict,True)