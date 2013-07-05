def setupHybrid(os,utils):
#------------------------------------------------
#Sets up the input matrices for the synthesizer
#------------------------------------------------
    buildHybridTrainingMatrix(utils.PROCESSED_CV_PATH,
                     utils.CVPredictionPaths,
                     utils.HYBRID_TRAIN_MATRIX_PATH,
                     utils.grabCSVColumn)
    buildHybridPredictorMatrix(utils.testPredictionPaths,
                               utils.grabCSVColumn,
                               utils.HYBRID_PREDICT_MATRIX_PATH)

def runHybrid(os,utils,HYBRID_CHOICE):
#-------------------------------------------------
# Calls an R script which uses the train and predict matrices
# To generate a prediction
#-------------------------------------------------
    print("Generating Results")
    if HYBRID_CHOICE==1:
        print("Hybrid Choice: OLS Regression")
        os.system('R CMD BATCH PostProcess/hybridOLS.R')
    if HYBRID_CHOICE==2:
        print("Hybrid Choice: Ridge Regression")
        os.system('R CMD BATCH PostProcess/hybridRR.R')

def buildHybridTrainingMatrix(processedCVPath,predictorPaths,outputPath,grabCSVColumnFunc):
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

def buildHybridPredictorMatrix(testPredictionPaths,grabCSVColumnFunc,outputPath):
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
