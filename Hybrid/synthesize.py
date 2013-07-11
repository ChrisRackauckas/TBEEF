import hybrid
from SynthModel import SynthModel
def setupSynthesize(utils,CVPredictionPaths,testPredictionPaths,configModel,trials,modelList,mproc,processes):
    processes = []
    for trial in range(0,trials):
        strTrial = str(trial)
        p = mproc.Process(target=synthSetupTrial,
                        args=(utils.SYNTH_ORIGINAL_PATH,strTrial,
                        utils.HYBRID_BOOT_PATH,
                        CVPredictionPaths[trial],
                        testPredictionPaths[trial],
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
        
        
def synthSetupTrial(synthOriginalPath,strTrial,hybridBootPath,CVPredictionPaths,testPredictionPaths,grabCSVColumnFunc,buildTrainingMatrixFromPredictionsFunc,buildPredictorMatrixFromPredictionsFunc,addHeaderFunc): 
        synthOriginal = synthOriginalPath \
                    + 'train_t' + strTrial
        synthPredict  = synthOriginalPath \
                    + 'test_t'  + strTrial

        buildTrainingMatrixFromPredictionsFunc(hybridBootPath + 
                    'CV_t' + strTrial + '_tmp', synthOriginal + '_tmp',
                    CVPredictionPaths,grabCSVColumnFunc)
        buildPredictorMatrixFromPredictionsFunc(testPredictionPaths,
                    grabCSVColumnFunc,synthPredict + '_tmp')
        addHeaderFunc(synthOriginal + '_tmp', synthOriginal,False)
        addHeaderFunc(synthPredict  + '_tmp', synthPredict,True)
 
