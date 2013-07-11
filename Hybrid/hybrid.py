def setupHybrid(utils,config,random,split,CVPredictionPaths,testPredictionPaths,modelList,trials):
    from HybridModel import HybridModel
    ### Setup data matrices and construct hybrid models ###

    for trial in range(0,trials):
        hybridOriginal = utils.HYBRID_ORIGINAL_PATH \
                            + 'train_t' + str(trial)
        hybridPredict = utils.HYBRID_ORIGINAL_PATH \
                            + 'test_t' + str(trial) + '_tmp'
        bootCV = utils.MODEL_BOOT_PATH  +   \
                                      'CV' + '_t' + str(trial)
        buildTrainingMatrixFromPredictions(bootCV,hybridOriginal,
                         CVPredictionPaths[trial],utils.grabCSVColumn)
        buildPredictorMatrixFromPredictions(testPredictionPaths[trial],
                         utils.grabCSVColumn,hybridPredict)
        utils.bootsplit(hybridOriginal,hybridOriginal + '_tmp',
                utils.HYBRID_BOOT_PATH + 'train_t' + str(trial) + '_tmp',
                utils.HYBRID_BOOT_PATH + 'CV_t'    + str(trial) + '_tmp',
                split,random)
        addHeader(utils.HYBRID_BOOT_PATH + 'train_t' + str(trial) + '_tmp',
                  utils.HYBRID_BOOT_PATH + 'train_t' + str(trial),False)
        addHeader(utils.HYBRID_BOOT_PATH + 'CV_t'    + str(trial) + '_tmp',
                  utils.HYBRID_BOOT_PATH + 'CV_t'    + str(trial),False)
        addHeader(utils.HYBRID_ORIGINAL_PATH + 
                  'test_t'    + str(trial) + '_tmp',
                  utils.HYBRID_ORIGINAL_PATH + 
                  'test_t'    + str(trial),True)

        for configModel in config.ensembleModels:
            model = HybridModel(configModel,utils,str(trial))
            modelList.append(model)

def buildTrainingMatrixFromPredictions(fullSet,outputPath,predictorPaths,grabCSVColumnFunc):
#-------------------------------------------------
# Takes in the prediction of various models on CV data
# Through CVPredictionPaths array
# Generates a txt file that is a matrix for training Hybrid
#-------------------------------------------------
    predictionArrays = [grabCSVColumnFunc(fullSet,2)]
    for predictPath in predictorPaths:
        predictionArrays.append(grabCSVColumnFunc(predictPath,2))
    toWrite = []
    for i in range(0,len(predictionArrays[0])):
        rowStr = predictionArrays[0][i]
        for j in range(1,len(predictionArrays)):
            rowStr = rowStr + "\t" + predictionArrays[j][i]
        rowStr = rowStr + "\n"
        toWrite.append(rowStr)
    outfile = open(outputPath, 'w')
    outfile.writelines(["%s" % row  for row in toWrite])

def buildPredictorMatrixFromPredictions(testPredictionPaths,grabCSVColumnFunc,outputPath):
#-------------------------------------------------
# Takes in the prediction of various models on test data
# Through testPredictionPaths array
# Generates a txt file that is a matrix for training Hybrid
#-------------------------------------------------
    predictionArrays = []
    for predictPath in testPredictionPaths:
        predictionArrays.append(grabCSVColumnFunc(predictPath,2))
    toWrite = []
    for i in range(0,len(predictionArrays[0])):
        rowStr = predictionArrays[0][i]
        for j in range(1,len(predictionArrays)):
            rowStr = rowStr + "\t" + predictionArrays[j][i]
        rowStr = rowStr + "\n"
        toWrite.append(rowStr)
    outfile = open(outputPath, 'w')
    outfile.writelines(["%s" % row  for row in toWrite])
    
def addHeader(inputPath, outputPath,testSet):
    inData = open(inputPath, 'r')
    outData= open(outputPath,'w')
    if testSet:
        header = "x1"
        additional = 1
    else :
        header = "y"
        additional = 0
    inLines = inData.readlines()
    numCols = len(inLines[0].split())
    toWrite = []
    for i in range(1,numCols):
        istr = str(i+additional)
        header = header + "\tx" + istr
    header = header + "\n"
    toWrite.append(header)
    toWrite.extend(inLines)
    outData.writelines(["%s" % row for row in toWrite])

