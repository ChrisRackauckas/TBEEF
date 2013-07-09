from Model import Model
class FMModel(Model):
   
### Constructors ########
    
    def __init__(self,configModel,utils,config,strTrial):
        super(FMModel,self).__init__(configModel,utils,strTrial)
        self.dims = configModel[3][0]
        self.logCV          = utils.MODEL_LOG_PATH      + self.tag + \
                                      '_CV' + '_t' + strTrial
        self.logTest        = utils.MODEL_LOG_PATH      + self.tag + \
                                    '_test' + '_t' + strTrial
        self.libFMBinary            = utils.LIBFM_BINARY
        self.strItr                = config.FM_STR_ITER
        self.globalBias             = utils.FM_GLOBAL_BIAS
        self.oneWay                 = utils.FM_ONE_WAY_INTERACTION
        self.initStd                = config.FM_INIT_STD
### Setup Data ###

    def setup(self):
        ### Take boot to feat ###
        print("Setting Up Features")
        self.setupFeatures()
        ### Take feat to bin to run ###
        print("Converting Data")
        self.dataConvert()

    def dataConvert(self):
        #-----------------------------
        # Takes in the raw data from original
        # Makes the .libfm sparse matrix
        # Then converts it to the binary form
        #-----------------------------
        import os
        os.system('perl Models/libFM/triple_format_to_libfm.pl -in ' + 
            self.featTrain  + ',' + 
            self.featTest + ',' + 
            self.featCV + 
            ' -target 2 -separator \"\\t\"')
        os.system('./Models/libFM/convert --ifile ' + 
            self.featTrain + 
            '.libfm ' + '--ofilex ' + 
            self.tmpTrain + 
            '.x --ofiley ' + 
            self.runTrain + '.y' +
            '> /dev/null') 
        os.system('./Models/libFM/convert --ifile ' + 
            self.featCV + 
            '.libfm ' + '--ofilex ' + 
            self.tmpCV +
            '.x --ofiley ' + 
            self.runCV + '.y' +
            '> /dev/null')
        os.system('./Models/libFM/convert --ifile ' + 
            self.featTest + 
            '.libfm ' + '--ofilex ' + 
            self.tmpTest + 
            '.x --ofiley ' + 
            self.runTest + '.y'
            '> /dev/null')
        os.system('./Models/libFM/transpose --ifile ' + 
            self.tmpTrain + 
            '.x --ofile ' + 
            self.runTrain + '.xt' +
            '> /dev/null')
        os.system('./Models/libFM/transpose --ifile ' + 
            self.tmpTest + 
            '.x --ofile ' + 
            self.runTest + '.xt' +
            '> /dev/null')
        os.system('./Models/libFM/transpose --ifile ' + 
            self.tmpCV + '.x --ofile ' + 
            self.runCV + '.xt' + 
            '> /dev/null')  

### Develop Features ###

    def setupFeatures(self):
        import os
        #-----------------------------------------------------------------
        # creates the features for LibFM
        #----------------------------------------------------------------- 
        if self.featureSet == 'Basic':
            os.system('cp ' + self.bootTrain + ' ' + self.featTrain)
            os.system('cp ' + self.bootCV    + ' ' + self.featCV   )
            os.system('cp ' + self.bootTest  + ' ' + self.featTest )

        if self.featureSet == 'MOVIE_TAG':
            print('Movie Tag data')
            self.addMovieMeta(self.bootTrain,self.featTrain)
            self.addMovieMeta(self.bootCV,self.featCV)
            self.addMovieMeta(self.bootTest,self.featTest)

    def addMovieMeta(self,finPath, foutPath):
        import os
        #-----------------------------------------------------------------
        # creates new data set with movie tag feature for LibFM
        #-----------------------------------------------------------------

        movieTags = open(self.MOVIE_TAG_PATH, 'r')
        tagDict = {}
        for line in movieTags:
            if line != '\n':
                line = line.replace('\n', '')
                columns = line.split('\t')
                movie = columns[0]
                allTags = columns[1]
                allTags = allTags.replace(',', '\t')
                tagDict[movie]=allTags
        dataSet = open(finPath,'r')
        dataSetWithTags = open(foutPath,'w')
        for line in dataSet:
            if line != '\n':
                line = line.replace('\n', '')
                columns = line.split('\t')
                movie = columns[1]
                if movie in tagDict:
                    dataSetWithTags.write(line+'\t'+tagDict.get(movie)+'\n')
                else:
                    dataSetWithTags.write(line+'\n')
        movieTags.close()
        dataSet.close()
        dataSetWithTags.close()
        os.system('mv '+foutPath+' '+ finPath)

### Run ###

    def run(self,sproc,subprocesses):
        fout_test_temp = self.predTest  + '_temp'
        fout_cv_temp   = self.predCV    + '_temp'

        cvStr = self.libFMBinary + ' -task r -train ' + \
            self.runTrain + ' -test ' + \
            self.runCV + ' -init_stdev ' + \
            self.initStd + ' -dim \'' + \
            self.globalBias + ','+ \
            self.oneWay + ','+ \
            self.dims + '\' -iter ' + \
            self.strItr + ' -rlog '+  \
            self.logCV + ' -out ' + \
            fout_cv_temp
        cvArr = cvStr.split()
        testStr = self.libFMBinary + ' -task r -train ' + \
            self.runTrain + ' -test ' + \
            self.runTest + ' -init_stdev ' + \
            self.initStd + ' -dim \'' + \
            self.globalBias + ','+ \
            self.oneWay + ','+ \
            self.dims + '\' -iter ' + \
            self.strItr + ' -rlog '+  \
            self.logTest + ' -out ' + \
            fout_test_temp
        testArr = testStr.split()
        ### CV ###
        pCV = sproc.Popen(cvArr,shell=False)
        pTest = sproc.Popen(testArr,shell=False)
        subprocesses.append(pTest)
        subprocesses.append(pCV)

    def fixRun(self):
        self.prependUserMovieToPredictions(self.bootTest,
                self.predTest + '_temp',
                self.predTest)

        self.prependUserMovieToPredictions(self.bootCV,
                self.predCV + '_temp',
                self.predCV)

