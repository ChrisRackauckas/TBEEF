from HybridModel import HybridModel

class SynthModel(HybridModel):
    def __init__(self,configModel,utils,strTrial):
        self.tag        = configModel[0]
        self.mode       = configModel[1]
        self.misc       = configModel[2]
        self.trial      = strTrial
        
        self.bootTest   = utils.TEST_IDS_PATH
        self.runTrain   = utils.SYNTH_ORIGINAL_PATH \
                          + 'train_t' + strTrial
        self.runTest    = utils.SYNTH_ORIGINAL_PATH \
                          + 'test_t'  + strTrial
        self.runCV      = self.runTest

        self.predTest   = utils.SYNTH_PREDICT_PATH \
                          + 't' + strTrial

        self.predCV     = self.predTest
        self.predTestTmp= self.predTest + '_tmp'
        self.predCVTmp  = self.predTestTmp
        self.log        = utils.SYNTH_LOG_PATH + self.tag + '_t' \
                          + strTrial
        self.CVSet = False
        self.setupRVars(utils)
