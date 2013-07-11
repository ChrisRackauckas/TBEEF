from Model import Model

class HybridModel(Model):
    def __init__(self,configModel,utils,strTrial): 
        self.tag        = configModel[0]
        self.mode       = configModel[1]
        self.misc       = configModel[2]
        self.trial      = strTrial

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
        self.setupRVars(utils)
        self.CVSet      = True

    def setupRVars(self,utils):
        import os
        self.OLS        = 'Hybrid/hybridOLS.R '
        self.RR         = 'Hybrid/hybridRR.R '
        self.RCatch     = self.runTrain + ' ' + self.runCV +\
                          ' ' + self.runTest + ' ' + self.predCVTmp \
                          + ' ' + self.predTestTmp  
        #self.logCall    =' > ' + self.log + \
        #                  ' 2>&1'
        self.RscriptPath= os.path.abspath('Rscript')
        
    def run(self,sproc,subprocesses):  
        progCall = 'Rscript ' + self.OLS + self.RCatch
        progArr = progCall.split()
        if self.mode == 'OLS':
            print("Hybrid Choice: OLS Regression")
            p = sproc.Popen(progArr,shell=False)
        if self.mode == 'OLSR':
            print("Hybrid Choice: Ridge Regression")
            p = sproc.Popen([self.RCall + self.RR 
                            + self.RCatch + self.logCall],shell=False)
        subprocesses.append(p)

