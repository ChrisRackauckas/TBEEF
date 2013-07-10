def setupHybrid(utils,config,random,split,CVPredictionPaths,testPredictionPaths,modelList,trials):
    from HybridModel import HybridModel
    ### Setup data matrices and construct hybrid models ###

    for trial in range(0,trials):
        hybridOriginal = utils.HYBRID_ORIGINAL_PATH \
                            + '_train_t' + str(trial)
        hybridPredict = utils.HYBRID_ORIGINAL_PATH \
                            + '_test_t' + str(trial)
        bootCV = utils.MODEL_BOOT_PATH  +   \
                                      '_CV' + '_t' + str(trial)
        buildTrainingMatrixFromPredictions(bootCV,hybridOriginal,
                         CVPredictionPaths[trial],utils.grabCSVColumn)
        buildPredictorMatrixFromPredictions(testPredictionPaths[trial],
                         utils.grabCSVColumn,hybridPredict)
        utils.bootsplit(hybridOriginal,hybridOriginal + '_tmp',
                utils.HYBRID_BOOT_PATH + '_train_t' + str(trial),
                utils.HYBRID_BOOT_PATH + '_CV_t'    + str(trial),
                split,random) 
        for configModel in config.ensembleModels:
            model = HybridModel(configModel,utils,str(trial))
            modelList.append(model)


def runHybrid(sproc,subprocesses,modelList):
#-------------------------------------------------
# Calls an R script which uses the train and predict matrices
# To generate a prediction
#-------------------------------------------------
    for model in modelList:
        model.run(sproc,subprocesses)

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
    header = "y"
    for i in range(1,len(predictionArrays)):
        istr = str(i)
        header = header + "\tx" + istr
    header = header + "\n"
    toWrite.append(header)
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
    header = "x1"
    for i in range(1,len(predictionArrays)):
        istr = str(i+1)
        header = header + "\tx" + istr
    header = header + "\n"
    toWrite.append(header)
    for i in range(0,len(predictionArrays[0])):
        rowStr = predictionArrays[0][i]
        for j in range(1,len(predictionArrays)):
            rowStr = rowStr + "\t" + predictionArrays[j][i]
        rowStr = rowStr + "\n"
        toWrite.append(rowStr)
    outfile = open(outputPath, 'w')
    outfile.writelines(["%s" % row  for row in toWrite])
