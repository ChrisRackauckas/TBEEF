def setupHybrid(os,utils):
#------------------------------------------------
#Sets up the input matrices for the synthesizer
#------------------------------------------------
    utils.aggregatePredictions(utils.TEST_IDS_PATH,
                         utils.HYBRID_TRAIN_MATRIX_PATH,
                         True,
                         utils.CVPredictionPaths[0])
    utils.aggregatePredictions(utils.ORIGINAL_DATA_CLEAN_PATH,
                         utils.HYBRID_PREDICT_MATRIX_PATH,
                         False,
                         utils.testPredictionPaths[0])
def runHybrid(os,utils,config,mproc):
#-------------------------------------------------
# Calls an R script which uses the train and predict matrices
# To generate a prediction
#-------------------------------------------------
    print("Generating Results")
    for model in config.ensembleModels:
        tag = model[0]
        bootTrain = utils.HYBRID_BOOT_PATH + tag + '_train'
        bootTest  = utils.HYBRID_BOOT_PATH + tag + '_test'
        logFile   = utils.HYBRID_LOG_PATH  + tag
        predPath  = utils.HYBRID_PRED_PATH + tag 
        hybridPaths = [bootTrain,bootTest,logFile]
        if model[1] == 'OLS':
            print("Hybrid Choice: OLS Regression")
            os.system('R CMD BATCH Hybrid/hybridOLS.R')
        if HYBRID_CHOICE==2:
            print("Hybrid Choice: Ridge Regression")
            os.system('R CMD BATCH Hybrid/hybridRR.R ')

def buildTrainingMatrixFromPredictions(fullSet,predictorPaths,outputPath,grabCSVColumnFunc):
#-------------------------------------------------
# Takes in the prediction of various models on CV data
# Through CVPredictionPaths array
# Generates a txt file that is a matrix for training Hybrid
#-------------------------------------------------
    predictionArrays = [grabCSVColumnFunc(processedCVPath,2)]
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
