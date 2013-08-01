from Model import Model

class HybridModel(Model):
    def __init__(self,configModel,utils,strTrial): 
        self.tag        = configModel[0]
        self.mode       = configModel[1]
        self.misc       = configModel[2]
        self.trial      = strTrial
        self.masterTest = utils.TEST_IDS_PATH
        self.runTrain   = utils.HYBRID_BOOT_PATH     + 'train_t' + strTrial
        self.runCV      = utils.HYBRID_BOOT_PATH     + 'CV_t'    + strTrial
        self.runTest    = utils.HYBRID_ORIGINAL_PATH + 'test_t'  + strTrial
        
        self.bootTrain  = self.runTrain + '_tmp'
        self.bootCV     = self.runCV    + '_tmp'
        self.bootTest   = self.runTest  + '_tmp'
        self.predCV     = utils.HYBRID_PREDICT_PATH  + self.tag \
                          + '_CV_t'    + strTrial
        self.predTest   = utils.HYBRID_PREDICT_PATH  + self.tag \
                          + '_test_t'  + strTrial
        self.predCVTmp  = self.predCV   + '_tmp'
        self.predTestTmp= self.predTest + '_tmp'
        self.log        = utils.HYBRID_LOG_PATH + self.tag + '_t'\
                                                + strTrial
        self.RMSEPath   = utils.HYBRID_RMSE_PATH+ self.tag + '_t'\
                                                + strTrial
        self.setupRVars(utils)

    def setupRVars(self,utils):
        self.miscStr        = ' '.join(map(str,self.misc))
        self.ensemblePath   = 'Hybrid/ensembles.R '
        self.RCatch         = self.runTrain + ' ' + self.runCV +\
                            ' ' + self.runTest + ' ' + self.predCVTmp \
                            + ' ' + self.predTestTmp + ' ' \
                            + self.RMSEPath + ' ' + self.mode \
                            + ' ' + self.miscStr

    def run(self,sproc,subprocesses):
        progCall = 'Rscript ' + self.ensemblePath + self.RCatch
        progArr = progCall.split()
        logFile = open(self.log,'w')
        p = sproc.Popen(progArr,shell=False,
                        stderr=logFile,stdout=logFile)
        subprocesses.append(p)


