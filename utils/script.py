def setupImplicitFeatures(self):
    import os
    #reindex the training files and build two dicts
    Udic,ItemDic,avg=reIndex_Implicit(self.bootTrain,self.tmpTrain)
    #reindex the history
    transalte(self.userHistoryPath, self.userHistoryReindexPath, Udic, ItemDic)
    #reindex CV file
    translate(self.bootCV, self.tmpCV, Udic, ItemDic)
    #reindex Testfile
    translate(self.bootTest, self.tmpTest, Udic, ItemDic)

    #make group training files
    os.system(self.SVDFeatureLineReorder +' '+ self.tmpTrain + \
            ' '+ self.tmpLineOrder)
    os.system(self.SVDFeatureSVDPPRandOrder + ' ' + self.tmpTrain + \
            ' ' + self.tmpLineOrder + ' ' + self.tmpGpTrain）

    #make group training files of the CV set
    os.system(self.SVDFeatureLineReorder +' '+ self.tmpCV + \
            ' '+ self.tmpLineOrder)
    os.system(self.SVDFeatureSVDPPRandOrder + ' ' + self.tmpCV + \
            ' ' + self.tmpLineOrder + ' ' + self.tmpGpCV）

    #make basic feature files
    self.basicConvert(self.tmpGpTrain,self.featTrain)
    self.basicConvert(self.tmpGpCV,   self.featCV)
    self.basicConvert(self.tmpTest, self.featTest)

    #make implicit feature files
    mkImplicitFeatureFile(self.userHistoryReindexPath,self.tmpGpTrain,self.ImfeatTrain)
    mkImplicitFeatureFile(self.userHistoryReindexPath,self.tmpTest,self.ImfeatTest)
    mkImplicitFeatureFile(self.userHistoryReindexPath,self.tmpGpCV,self.ImfeatCV)

    #set different parameters
    self.numUser=len(Udic)
    self.numMovie=len(ItemDic)
    self.avg=avg
    self.numGlobal = 0
    self.activeType = 0
    self.formatType = 1
    self.numUserFeedback = len(ItemDic)
    
