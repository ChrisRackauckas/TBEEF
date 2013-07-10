class HybridModel(object):
    def __init__(self,configModel,utils,strTrial):
        self.tag        = configModel[0]
        self.mode       = configModel[1]
        self.misc       = configModel[2]
        self.trial      = strTrial

        self.bootTrain  = utils.HYBRID_BOOT_PATH     + '_train_t' + strTrial
        self.bootCV     = utils.HYBRID_BOOT_PATH     + '_CV_t'    + strTrial
        self.bootTest   = utils.HYBRID_ORIGINAL_PATH + '_test_t'  + strTrial
        
        self.log        = utils.HYBRID_LOG_PATH + self.tag + '_t'\
                                                + strTrial
        self.OLS        = 'Hybrid/hybridOLS.R '
        self.RCatch     = '--no-save --no-restore --verbose --args ' + \
                          self.bootTrain + ' ' + self.bootCV +\
                          ' ' + self.bootTest + ' > ' + \
                          self.log + ' 2>&1'

    def run(self,sproc,subprocesses):
        import os
        print("in here!")
        print('R' + self.OLS + self.RCatch) 
        if self.mode == 'OLS':
            print("Hybrid Choice: OLS Regression")
            os.system('R ' + self.OLS + self.RCatch)
        if self.mode == 'OLSR':
            print("Hybrid Choice: Ridge Regression")
            os.system('R CMD BATCH Hybrid/hybridRR.R ')


