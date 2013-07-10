import hybrid
from SynthModel import SynthModel
def setupSynthesize(utils,CVPredictionPaths,testPredictionPaths,configModel,trials,modelList):
    for trial in range(0,trials):
        strTrial = str(trial)
        synthOriginal = utils.SYNTH_ORIGINAL_PATH \
                    + 'train_t' + strTrial
        synthPredict  = utils.SYNTH_ORIGINAL_PATH \
                    + 'test_t'  + strTrial

        hybrid.buildTrainingMatrixFromPredictions(utils.HYBRID_BOOT_PATH + 
                    'CV_t' + strTrial + '_tmp', synthOriginal + '_tmp',
                    CVPredictionPaths[trial],utils.grabCSVColumn)
        hybrid.buildPredictorMatrixFromPredictions(testPredictionPaths[trial],
                    utils.grabCSVColumn,synthPredict + '_tmp')
        hybrid.addHeader(synthOriginal + '_tmp', synthOriginal,False)
        hybrid.addHeader(synthPredict  + '_tmp', synthPredict,True)
        
        synthModel = SynthModel(configModel,utils,strTrial)
        modelList.append(synthModel)
