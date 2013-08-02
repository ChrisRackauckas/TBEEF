def setupHybrid(utils,config,mproc,random,split,CVPredictionPaths,testPredictionPaths,modelList,trials):
    from HybridModel import HybridModel
    ### Setup data matrices and construct hybrid models ###
    processes = []
    for trial in range(0,trials):
        p = mproc.Process(target=setupHybridTrial,
                args=(utils.HYBRID_ORIGINAL_PATH,
                    str(trial),utils.MODEL_BOOT_PATH,
                    CVPredictionPaths[trial],random,split,
                    utils.bootsplit,utils.grabCSVColumn,
                    testPredictionPaths[trial],utils.HYBRID_BOOT_PATH))
        p.start()
        processes.append(p)
        for configModel in config.ensembleModels:
            model = HybridModel(configModel,utils,str(trial))
            modelList.append(model)
    
    for p in processes:
        p.join()

def setupHybridTrial(hybridOriginalPath,strTrial,modelBootPath,CVPredictionPaths,random,split,bootsplitFunc,grabCSVColumnFunc,testPredictionPaths,hybridBootPath):    
    hybridOriginal = hybridOriginalPath \
                        + 'train_t' + strTrial
    hybridPredict  = hybridOriginalPath \
                        + 'test_t' + strTrial + '_tmp'
    bootCV = modelBootPath  +   \
                        'CV' + '_t' + strTrial
    buildTrainingMatrixFromPredictions(bootCV,hybridOriginal,
                        CVPredictionPaths,grabCSVColumnFunc,2)
    buildPredictorMatrixFromPredictions(testPredictionPaths,
                        grabCSVColumnFunc,hybridPredict)
    bootsplitFunc(hybridOriginal,hybridOriginal + '_tmp',
                hybridBootPath + 'train_t' + strTrial + '_tmp',
                hybridBootPath + 'CV_t'    + strTrial + '_tmp',
                split,random)
    addHeader(hybridBootPath + 'train_t' + strTrial + '_tmp',
                hybridBootPath + 'train_t' + strTrial,False)
    addHeader(hybridBootPath + 'CV_t'    + strTrial + '_tmp',
                hybridBootPath + 'CV_t'    + strTrial,False)
    addHeader(hybridOriginalPath + 
                'test_t'    + strTrial + '_tmp',
                hybridOriginalPath + 
                'test_t'    + strTrial,True)

def buildTrainingMatrixFromPredictions(fullSet,outputPath,predictorPaths,grabCSVColumnFunc,masterColumn):
#-------------------------------------------------
# Takes in the prediction of various models on CV data
# Through CVPredictionPaths array
# Generates a txt file that is a matrix for training Hybrid
#-------------------------------------------------
    predictionArrays = [grabCSVColumnFunc(fullSet,masterColumn)]
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

