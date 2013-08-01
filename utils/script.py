def setupImplicitFeatures(self):
    #translate the training files and build two dicts
    Udic,ItemDic,avg=reIndex_Implicit(self.bootTrain,self.tmpTrain)
    #translate CV file
    translate(self.bootCV, self.tmpCV, Udic, ItemDic)
    #translate Testfile
    translate(self.bootTest, self.tmpTest, Udic, ItemDic)

    #set different parameters
    self.numUser=len(UDic)
    self.numMovie=len(ItemDic)
    self.avg=avg
    self.numGlobal = 0

    #make basic feature files
    self.basicConvert(self.tmpTrain,self.featTrain)
    self.basicConvert(self.tmpCV,   self.featCV)
    self.basicConvert(self.tmpTest, self.featTest)
    
    #make implicit feature files
    #Here I need to issue two command
    #
