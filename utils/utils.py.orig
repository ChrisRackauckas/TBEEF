#### Paths ####

template = 'bin/libFM -task r -train training_set_nodups.libfm -test predict_dummy.libfm -dim ’1,1,8’ -out colin_test8.txt'
TEST_IDS_PATH = 'Data/Original/predict.txt'
TEST_IDS_DUMMY_PATH = 'Data/PreProcessed/predict_dummy.txt'
PROCESSED_TRAIN_PATH = 'Data/PreProcessed/training_set_processed.txt'
PROCESSED_CV_PATH = 'Data/PreProcessed/cv_set_processed.txt'

testPredictionPaths = [] #Array of paths where test predictions are saved
CVPredictionPaths = [] #Array of paths where CV predictions are saved

#### FM ####

FM_TRAIN_PATH = 'Data/ModelData/FMTrain.txt'
FM_TEST_PATH = 'Data/ModelData/FMTest.txt'
FM_CV_PATH = 'Data/ModelData/FMCV.txt'
FM_ITER = 5
FM_STR_ITER = str(FM_ITER)
FM_GLOBAL_BIAS = '1' #either 1 or 0
FM_ONE_WAY_INTERACTION = '1' #either 1 or 0
FM_PREDICTIONS_PATH = 'Data/ModelPredictions/'
FM_DIMS = [ '1', '2']

#### Hybrid ####

HYBRID_TRAIN_MATRIX_PATH    = 'Data/Hybrid/hybridTrain.txt'
HYBRID_PREDICT_MATRIX_PATH  = 'Data/Hybrid/hybridPredict.txt'
HYBRID_SYNTHESIZED_PATH     = 'Data/Hybrid/hybridSynthesized.txt'
OUTPUT_PATH                 = 'Data/Output/output.txt'

#### Utility Functions ####

def grabCSVColumn(csv_path,columnNumber):
	import csv
	data = csv.reader(open(csv_path), delimiter="\t", quotechar='|')
	ans = []
	for row in data:
		ans.append(row[columnNumber])
	return ans

def fixTestPredictions(utils,toFix,toSave):
    
    ids = open(utils.TEST_IDS_PATH, 'r')
    predictions = open(toFix, 'r')
    idlines = ids.readlines();
    plines = predictions.readlines();
    maxX = len(idlines)-1

    output = [];
    for x in range(0,maxX) :
        if x == maxX:
            output.append(idlines[x] + "\t" + plines[x])
        else :
            output.append(idlines[x][:-2] + "\t" + plines[x])
    outfile = open(toSave, 'w')
    outfile.writelines(["%s" % item  for item in output])