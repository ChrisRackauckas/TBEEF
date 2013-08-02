from Model import Model
import ImplicitFeedbackFunctions as IFF #IFF for implicitFeedbackFunctions
import neighborhoodFunctions as NF 
class SVDModel(Model):

### Construct ###    

    def __init__(self,configModel,utils,config,strTrial):
	    #This function is to set up different parameters.
        Model.__init__(self,configModel,utils,strTrial) 
        self.configPath = utils.MODEL_CONFIG_PATH   + self.tag + \
                                              '_t' + strTrial
        
        ### Baidu Specific ###
        ### Implicit Feedback Files ###
        self.userHistoryReindexPath= utils.MODEL_TMP_PATH      + self.tag + \
                                     '_userHistoryReindex' + '_t' + strTrial
        #The following 3 files are implicit feature files
        self.ImfeatTrain  = utils.MODEL_FEATURED_PATH + self.tag + \
                            '_Imtrain' + '_t' + strTrial
        self.ImfeatCV     = utils.MODEL_FEATURED_PATH + self.tag + \
                            '_ImCV' + '_t' + strTrial
        self.ImfeatTest   = utils.MODEL_FEATURED_PATH + self.tag + \
                            '_Imtest' + '_t' + strTrial
        #Gp for group training file, the test file is already in group format,so skip it
        self.tmpGpTrain   = utils.MODEL_TMP_PATH      + self.tag + \
                            '_Gptrain' + '_t' + strTrial
        self.tmpGpCV   = utils.MODEL_TMP_PATH      + self.tag + \
                         '_GpCV' + '_t' + strTrial
        #for storing the line order of the group file
        self.tmpLineOrder = utils.MODEL_TMP_PATH      + self.tag + \
                            '_LineOrder' + '_t' + strTrial
        ### End Implicit Feature Files ###

        self.regularizationFeedback = config.SVD_REGULARIZATION_FEEDBACK


        ### Neighborhood Model Files###
        if len(self.misc) > 0:
            if self.misc[0] == "MovieTag":
                self.TagFilePath = self.movieTagPath
                self.TagFileReindexPath = utils.MODEL_TMP_PATH      + self.tag + \
                                               '_' + self.misc[0] + '_t' + strTrial
                self.ShareTagPath = utils.MODEL_TMP_PATH      + self.tag + \
                                               '_share_' + self.misc[0] + '_t' + strTrial
        ### End Neighborhood Model Files###
        ### End Baidu Specific ###

        self.numIter              = config.SVD_NUM_ITER
        self.SVDBufferPath        = utils.SVDFEATURE_BUFFER_BINARY
        self.SVDGroupBufferPath   = utils.SVDFEATURE_GROUP_BUFFER_BINARY
        self.learningRate         = config.SVD_LEARNING_RATE
        self.regularizationItem   = config.SVD_REGULARIZATION_ITEM
        self.regularizationUser   = config.SVD_REGULARIZATION_USER
        self.regularizationGlobal = config.SVD_REGULARIZATION_GLOBAL
        self.numFactor            = config.SVD_NUM_FACTOR
        self.activeType           = config.SVD_ACTIVE_TYPE
        self.modelOutPath         = utils.SVDFEATURE_MODEL_OUT_PATH
        self.SVDFeatureBinary     = utils.SVDFEATURE_BINARY
        self.SVDFeatureInferBinary= utils.SVDFEATURE_INFER_BINARY
        self.SVDFeatureLineReorder= utils.SVDFEATURE_LINE_REORDER
        self.SVDFeatureSVDPPRandOrder = utils.SVDFEATURE_SVDPP_RANDORDER
        self.formatType           = 0
        self.numUserFeedback      = 0
        self.numUser= 0
        self.numMovie= 0
        self.numGlobal = 0
        self.avg= 0
        self.originDataSet        = utils.ORIGINAL_DATA_PATH 
        # 0 is the default value
        
### Setup Data ###

    def setup(self):
        import utils
        import config
        if self.featureSet == 'Basic':
            ### Boot to tmp ###
            print("Re-Indexing")
            values = self.reIndex()
        ### Take tmp to feat ###
        print("Setting Up Features")
        self.setupFeatures()
        ### Take feat to run ###
        print("Converting Data")
        self.dataConvert()
        ### Write config file ###
        print("Writing Config")
        self.writeConfig()

    def reIndex(self):
        bootTrainFile = open(self.bootTrain, 'r')
        bootCVFile    = open(self.bootCV   , 'r')
        bootTestFile  = open(self.bootTest , 'r')
        tmpTrainFile  = open(self.tmpTrain,  'w')
        tmpTestFile   = open(self.tmpTest,   'w')
        tmpCVFile     = open(self.tmpCV,     'w')

        ############## Write tmp file reindexed ###############3
        trainLines = bootTrainFile.readlines()
        CVLines    = bootCVFile.readlines()
        testLines  = bootTestFile.readlines()

        fullInput = []
        fullInput.append(trainLines)
        fullInput.append(CVLines)
        fullInput.append(testLines)

        uidDic={}
        iidDic={}
        newuid=1
        newiid=1
        ctr=0  # is the counter of the total number.
        sum=0.0

        #Build dictionary
    
        for line in trainLines:
            arr = line.rsplit('\t')
            uid = int(arr[0].strip())
            iid = int(arr[1].strip())
            rating = int(float(arr[2].strip()))
            #this part for calculating the average
            sum+=rating
            ctr+=1

		    #this part for reindexing the user ID
            if uid not in uidDic:
                uidDic[uid]=newuid
                newuid+=1
		    #this part for reindexing the item ID
            if iid not in iidDic:
                iidDic[iid]=newiid
                newiid+=1
    
        for line in CVLines:
            arr = line.rsplit('\t')
            uid = int(arr[0].strip())
            iid = int(arr[1].strip())
            #this part for reindexing the user ID
            if uid not in uidDic:
                uidDic[uid]=newuid
                newuid+=1
		    #this part for reindexing the item ID
            if iid not in iidDic:
                iidDic[iid]=newiid
                newiid+=1
    
        for line in testLines:
            arr = line.rsplit('\t')
            uid = int(arr[0].strip())
            iid = int(arr[1].strip())
	        #this part for reindexing the user ID
            if uid not in uidDic:
                uidDic[uid]=newuid
                newuid+=1
		    #this part for reindexing the item ID
            if iid not in iidDic:
                iidDic[iid]=newiid
                newiid+=1

        #Re-index
        for line in trainLines:
            arr = line.split()
            uid = int(arr[0].strip())
            iid = int(arr[1].strip())
            rating = int(float(arr[2].strip()))
            tmpTrainFile.write('%d\t%d\t%d\n' %(uidDic[uid],iidDic[iid],rating))
        for line in CVLines:
            arr = line.split()
            uid = int(arr[0].strip())
            iid = int(arr[1].strip())
            rating = int(float(arr[2].strip()))
            tmpCVFile.write('%d\t%d\t%d\n' %(uidDic[uid],iidDic[iid],rating))
        for line in testLines:
            arr = line.split()
            uid = int(arr[0].strip())
            iid = int(arr[1].strip())
            rating = int(float(arr[2].strip()))
            tmpTestFile.write('%d\t%d\t%d\n' %(uidDic[uid],iidDic[iid],rating))

        #calculate different parameter.
    
        self.numUser=len(uidDic)
        self.numMovie=len(iidDic)
        self.avg=sum/ctr
        self.numGlobal = 0
    
        #Close files
        bootTrainFile.close()
        bootTestFile.close()
        bootCVFile.close()
        tmpTrainFile.close()
        tmpTestFile.close()
        tmpCVFile.close()

    def dataConvert(self):
        import os
        if self.featureSet == 'Basic' or \
                self.featureSet == 'Neighborhood':
            os.system(self.SVDBufferPath + ' ' + 
                    self.featTrain + ' ' + self.runTrain)
            os.system(self.SVDBufferPath + ' ' + 
                    self.featCV    + ' ' + self.runCV   )
            os.system(self.SVDBufferPath + ' ' + 
                    self.featTest  + ' ' + self.runTest )
        if self.featureSet == 'ImplicitFeedback':
            os.system(self.SVDGroupBufferPath + ' ' + self.featTrain + \
                        ' ' + self.runTrain + ' ' + '-fd' + ' ' + self.ImfeatTrain)
            os.system(self.SVDGroupBufferPath + ' ' + self.featCV + \
                        ' ' + self.runCV + ' ' + '-fd' + ' ' + self.ImfeatCV)
            os.system(self.SVDGroupBufferPath + ' ' + self.featTest + \
                        ' ' + self.runTest + ' ' + '-fd' + ' ' + self.ImfeatTest)
    def writeConfig(self):
        import os
        fout =  open(self.configPath,'w')
        fout.write('#Config file for ' + self.tag + '\n')
        fout.write('#Global Bias\n')
        fout.write('base_score = '    + str(self.avg) + '\n')
        fout.write('#Learning Rate for SGD\n')
        fout.write('learning_rate = ' + self.learningRate + '\n')
        fout.write('#Regularization Constants (\lambda)\n')
        fout.write('wd_item = '       + self.regularizationItem + '\n')
        fout.write('wd_user = '       + self.regularizationUser + '\n')
        fout.write('wd_global = '     + self.regularizationGlobal+'\n')
        fout.write('#Numbers of Features\n')
        fout.write('num_item = '      + str(self.numMovie) + '\n')
        fout.write('num_user = '      + str(self.numUser)  + '\n')
        fout.write('num_global = '    + str(self.numGlobal)+ '\n')
        fout.write('#Number of features\n')
        fout.write('num_factor = '   + self.numFactor + '\n')
        fout.write('#Translation function: 0=linear, 2=sigmoid\n')
        fout.write('active_type = '   + self.activeType + '\n')
        fout.write('#Training dataset\n')
        fout.write('buffer_feature = \"' + self.runTrain + '\"\n')
        fout.write('#Model save path\n')
        fout.write('model_out_folder = \"' + self.modelOutPath
                + self.tag + '_t' + self.trial + '\"')
        if self.featureSet == 'ImplicitFeedback':
            fout.write('\n')
            fout.write("format_type = " + str(self.formatType) + '\n')
            fout.write("num_ufeedback = " + str(self.numUserFeedback) + '\n')
            fout.write("wd_ufeedback = " + self.regularizationFeedback + '\n')

        os.system('mkdir ' + self.modelOutPath 
                + self.tag + '_t' + self.trial)
        fout.close()

### Setup Features ###
    def setupFeatures(self):
        if self.featureSet == 'Basic':
            self.basicConvert(self.tmpTrain,self.featTrain)
            self.basicConvert(self.tmpCV,   self.featCV)
            self.basicConvert(self.tmpTest, self.featTest)
        ### Baidu Specific Features ###
        if self.featureSet == 'ImplicitFeedback':
            self.setupImplicitFeatures()
        if self.featureSet == 'Neighborhood':
            self.NeighborhoodSetup()
        ### End Baidu Specific Features ###

    def basicConvert(self,fin,fout):
        fi = open( fin , 'r' )
        fo = open( fout, 'w' )
        #extract from input file    
        for line in fi:
            arr  =  line.split()               
            uid  =  int(arr[0].strip())
            iid  =  int(arr[1].strip())
            score=  int(arr[2].strip())
            fo.write( '%d\t0\t1\t1\t' %score )
            # Print data,user and item features all start from 0
            fo.write('%d:1 %d:1\n' %(uid-1,iid-1))
        fi.close()
        fo.close()

    def setupImplicitFeatures(self):
        import os
        #reindex the training files and build two dicts
        Udic,ItemDic,avg=IFF.reIndex_Implicit(self.bootTrain, self.bootCV, self.bootTest, self.tmpTrain, self.tmpCV, self.tmpTest)
        #reindex the history
        IFF.translate(self.userHistoryPath, self.userHistoryReindexPath, Udic, ItemDic)

        #make group training files
        os.system(self.SVDFeatureSVDPPRandOrder +' '+ self.tmpTrain + ' ' + self.tmpLineOrder)
        os.system(self.SVDFeatureLineReorder + ' ' + self.tmpTrain + ' ' + self.tmpLineOrder + ' ' + self.tmpGpTrain)

        #make group training files of the CV set
        os.system(self.SVDFeatureSVDPPRandOrder +' '+ self.tmpCV + \
                  ' '+ self.tmpLineOrder)
        os.system(self.SVDFeatureLineReorder + ' ' + self.tmpCV + \
                  ' ' + self.tmpLineOrder + ' ' + self.tmpGpCV)

        #make basic feature files
        self.basicConvert(self.tmpGpTrain,self.featTrain)
        self.basicConvert(self.tmpGpCV,   self.featCV)
        self.basicConvert(self.tmpTest, self.featTest)

        #make implicit feature files
        IFF.mkImplicitFeatureFile(self.userHistoryReindexPath,self.tmpGpTrain,self.ImfeatTrain)
        IFF.mkImplicitFeatureFile(self.userHistoryReindexPath,self.tmpTest,self.ImfeatTest)
        IFF.mkImplicitFeatureFile(self.userHistoryReindexPath,self.tmpGpCV,self.ImfeatCV)


        #set different parameters
        self.numUser=len(Udic)
        self.numMovie=len(ItemDic)
        self.avg=avg
        self.numGlobal = 0
        self.activeType = '0'
        self.formatType = 1
        self.numUserFeedback = len(ItemDic)

    ### Run ###

    def run(self,sproc,subprocesses):
        p = sproc.Popen(self.SVDFeatureBinary + ' ' + self.configPath +
             ' num_round=' + self.numIter,shell=True) 
        subprocesses.append(p)

    def fixRun(self):
        import os
        self.predCVTmp   = self.predCV   + '_tmp'
        self.predTestTmp = self.predTest + '_tmp'
        os.system(self.SVDFeatureInferBinary + ' ' + self.configPath +
             ' test:buffer_feature=\"' + self.runCV + '\"' +
             ' pred=' + self.numIter + 
             ' name_pred=' + self.predCVTmp)
        os.system(self.SVDFeatureInferBinary + ' ' + self.configPath +
             ' test:buffer_feature=\"' + self.runTest + '\"'
             ' pred='      + self.numIter +
             ' name_pred=' + self.predTestTmp)
        self.prependUserMovieToPredictions(self.bootCV,self.predCVTmp,self.predCV)
        self.prependUserMovieToPredictions(self.bootTest,self.predTestTmp,self.predTest)       


    def NeighborhoodSetup(self):
        #second 
        NSnoUser,NSnoMovie,NSAvg = NF.reIndex(self.bootTrain, self.TagFilePath, self.bootTest, self.bootCV, self.tmpTrain, self.TagFileReindexPath, self.tmpTest, self.tmpCV)
        
        #third
        NF.share(self.TagFileReindexPath,self.ShareTagPath)

        #fourth
        NumGlobal = NF.neighborhood(self.tmpTrain, self.ShareTagPath, self.tmpTest, self.featTrain, self.featTest)
        NF.neighborhood(self.tmpCV, self.ShareTagPath, self.tmpTest, self.featCV, self.featTest)

        # set the parameters.
        self.numUser    =   NSnoUser
        self.numMovie   =   NSnoMovie
        self.numGlobal  =   NumGlobal + 1
        self.avg        =   NSAvg

