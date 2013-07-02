def setupHybrid(os,utils):
	setupHybridTrain(os,utils)
	setupHybridPredict(os,utils)

def runHybrid(os,utils):
#-------------------------------------------------
# Calls an R script which uses the train and predict matrices
# To generate a prediction
#-------------------------------------------------
    print("Generating Results")
    os.system('R CMD BATCH PostProcess/hybrid.R')



def setupHybridTrain(os,utils):
#-------------------------------------------------
# Takes in the prediction of various models on CV data
# Through CVPredictionPaths array
# Generates a txt file that is a matrix for training Hybrid
#-------------------------------------------------
	predictionArrays = [utils.grabCSVColumn(utils.PROCESSED_CV_PATH,2)]
	for predictPath in utils.CVPredictionPaths:
		predictionArrays.append(utils.grabCSVColumn(predictPath,2))
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
	outfile = open(utils.HYBRID_TRAIN_MATRIX_PATH, 'w')
	outfile.writelines(["%s" % row  for row in toWrite])

def setupHybridPredict(os,utils):
#-------------------------------------------------
# Takes in the prediction of various models on test data
# Through testPredictionPaths array
# Generates a txt file that is a matrix for training Hybrid
#-------------------------------------------------
	predictionArrays = []
	for predictPath in utils.testPredictionPaths:
		predictionArrays.append(utils.grabCSVColumn(predictPath,2))
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
	outfile = open(utils.HYBRID_PREDICT_MATRIX_PATH, 'w')
	outfile.writelines(["%s" % row  for row in toWrite])
