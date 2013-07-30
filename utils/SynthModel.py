from HybridModel import HybridModel

class SynthModel(HybridModel):
    def __init__(self,configModel,utils,strTrial):
        self.tag        = configModel[0]
        self.mode       = configModel[1]
        self.misc       = configModel[2]
        self.trial      = strTrial
        self.masterTest = utils.TEST_IDS_PATH
        self.runTrain   = utils.SYNTH_BOOT_PATH \
                          + 'train_t' + strTrial
        self.runCV      = utils.SYNTH_BOOT_PATH \
                          + 'CV_t'  + strTrial
        self.runTest    = utils.SYNTH_ORIGINAL_PATH \
                          + 'test_t'  + strTrial
        self.predTest   = utils.SYNTH_PREDICT_PATH \
                          + 't' + strTrial
        self.bootCV     = self.runCV    + '_tmp'
        self.predCV     = utils.SYNTH_PREDICT_PATH \
                          + 'CV_t' + strTrial
        self.predTestTmp= self.predTest + '_tmp'
        self.predCVTmp  = self.predCV   + '_tmp'
        self.log        = utils.SYNTH_LOG_PATH + self.tag + '_t' \
                          + strTrial
        self.RMSEPath   = utils.SYNTH_RMSE_PATH+ self.tag + '_t' \
                          + strTrial
        self.setupRVars(utils)
