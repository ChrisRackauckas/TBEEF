class Model(object):
    def __init__(self,configModel,utils,strTrial):
        self.tag        = configModel[0]
        self.mode       = configModel[1]
        self.featureSet = configModel[2]
        self.misc       = configModel[3]
        self.masterTest = utils.TEST_IDS_PATH
        self.bootTrain  =  utils.MODEL_BOOT_PATH  +   \
                                   'train' + '_t' + strTrial
        self.bootCV     =  utils.MODEL_BOOT_PATH  +   \
                                      'CV' + '_t' + strTrial
        self.bootTest   =  utils.MODEL_BOOT_PATH + \
                                    'test' + '_t' + strTrial  
        #The following will be regarded as basic feature files
        self.featTrain  = utils.MODEL_FEATURED_PATH + self.tag + \
                                        '_train' + '_t' + strTrial
        self.featCV     = utils.MODEL_FEATURED_PATH + self.tag + \
                                      '_CV' + '_t' + strTrial
        self.featTest   = utils.MODEL_FEATURED_PATH + self.tag + \
                                    '_test' + '_t' + strTrial

        #The following 3 files are implicit feature files
        self.ImfeatTrain  = utils.MODEL_FEATURED_PATH + self.tag + \
                                        '_Imtrain' + '_t' + strTrial
        self.ImfeatCV     = utils.MODEL_FEATURED_PATH + self.tag + \
                                      '_ImCV' + '_t' + strTrial
        self.ImfeatTest   = utils.MODEL_FEATURED_PATH + self.tag + \
                                    '_Imtest' + '_t' + strTrial

        self.tmpTrain   = utils.MODEL_TMP_PATH      + self.tag + \
                                   '_train' + '_t' + strtrial
        self.tmpCV      = utils.MODEL_TMP_PATH      + self.tag + \
                                      '_CV' + '_t' + strTrial
        #Gp for group training file, the test file is already in group format,so skip it
        self.tmpGpTrain   = utils.MODEL_TMP_PATH      + self.tag + \
                                   '_Gptrain' + '_t' + strtrial                 
        self.tmpGpCV   = utils.MODEL_TMP_PATH      + self.tag + \
                                   '_GpCV' + '_t' + strtrial

        self.tmpTest    = utils.MODEL_TMP_PATH      + self.tag + \
                                     '_test'+ '_t' + strTrial 
        #for storing the line order of the group file
        self.tmpLineOrder = utils.MODEL_TMP_PATH      + self.tag + \
                                   '_LineOrder' + '_t' + strTrial
                             
        self.runTrain   = utils.MODEL_RUN_PATH      + self.tag + \
                                   '_train' + '_t' + strTrial
        self.runCV      = utils.MODEL_RUN_PATH      + self.tag + \
                                      '_CV' + '_t' + strTrial
        self.runTest    = utils.MODEL_RUN_PATH      + self.tag + \
                                    '_test' + '_t' + strTrial
        self.predCV     = utils.MODEL_PREDICT_PATH  + self.tag + \
                                       '_CV'+ '_t' + strTrial
        self.predTest   = utils.MODEL_PREDICT_PATH  + self.tag + \
                                    '_test' + '_t' + strTrial
        self.predCVTmp  = self.predCV   + '_tmp'
        self.predTestTmp= self.predTest + '_tmp'
        self.trial      = strTrial
        self.movieTagPath   = utils.MOVIE_TAG_PATH
        self.userSocialPath = utils.USER_SOCIAL_PATH
        self.userHistoryPath= utils.USER_HISTORY_PATH
        self.userHistoryReindexPath= utils.MODEL_TMP_PATH      + self.tag + \
                '_userHistoryReindex' + '_t' + strTrial
        self.CVSet = True


    def prependUserMovieToPredictions(self,idsPath,fixPath,savePath):
        ### Takes in a column of ratings as toFix
        ### Takes in user and movie id's through idsPath
        ### Makes user movie rating and saves toSave
        ### ratingsCol is a boolean for implying
        ### whether the input for idsPath
        ### has a column of ratings or not
        import csv
        data = csv.reader(open(idsPath,'rU'), delimiter="\t", quotechar='|')
        fixData = open(fixPath, 'r')
        fixLines = fixData.readlines();
        i = 0
        output = [];
        for row in data :
            output.append(row[0] + '\t' + row[1] + "\t" + fixLines[i])
            i = i + 1
        outfile = open(savePath, 'w')
        outfile.writelines(["%s" % item  for item in output])
        
    def fixRun(self):
        self.prependUserMovieToPredictions(self.masterTest,
                self.predTestTmp,
                self.predTest)
        if self.CVSet:
            self.prependUserMovieToPredictions(self.bootCV,
                self.predCVTmp,
                self.predCV)

