#### Processes ####

processes = []

#### Paths ####

TEST_IDS_PATH = 'Data/Original/predict.txt'
TEST_IDS_DUMMY_PATH = 'Data/PreProcessed/predict_dummy.txt'
PROCESSED_TRAIN_PATH = 'Data/PreProcessed/training_set_processed.txt'
PROCESSED_CV_PATH = 'Data/PreProcessed/cv_set_processed.txt'

ORIGINAL_DATA_PATH = 'Data/Original/data_set.txt'
ORIGINAL_DATA_RNDM_NODUPS_PATH = 'Data/Original/data_set_nodups_rndm.txt'
PROCESSED_DATA_PATH = 'Data/PreProcessed/data_set_processed.txt'

EFFECTS_USER_PATH = 'Data/Effects/user_effects.txt'
EFFECTS_MOVIE_PATH = 'Data/Effects/movie_effects.txt'
EFFECTS_GLOBAL_PATH = 'Data/Effects/global_effects.txt'

testPredictionPaths = [] #Array of paths where test predictions are saved
CVPredictionPaths = [] #Array of paths where CV predictions are saved

#### DATA ####

DATA_SET_SPLIT = .8 #percent of data file for training, 1-value is cross val

#### FM ####

FM_TRAIN_BIN_PATH = 'Data/PreProcessed/FMTrainBin'
FM_TRAIN_PATH     = 'Data/ModelData/FMTrain.txt'
FM_TEST_BIN_PATH  = 'Data/PreProcessed/FMTestBin'
FM_TEST_PATH      = 'Data/ModelData/FMTest.txt'
FM_CV_BIN_PATH    = 'Data/PreProcessed/FMCVBin'
FM_CV_PATH        = 'Data/ModelData/FMCV.txt'
FM_ITER = 100
FM_STR_ITER = str(FM_ITER)
FM_GLOBAL_BIAS = '1' #either 1 or 0
FM_ONE_WAY_INTERACTION = '1' #either 1 or 0
FM_PREDICTIONS_PATH = 'Data/ModelPredictions/'
FM_DIMS = [ '1', '2']

#### Hybrid ####

HYBRID_TRAIN_MATRIX_PATH    = 'Data/Hybrid/hybridTrain.txt'
HYBRID_PREDICT_MATRIX_PATH  = 'Data/Hybrid/hybridPredict.txt'
HYBRID_SYNTHESIZED_PATH     = 'Data/Hybrid/hybridSynthesized.txt'
RE_EFFECT_PATH              = 'Data/Output/re_effect.txt' 
OUTPUT_PATH                 = 'Data/Output/output.txt'
TO_POST_PATH                = 'Data/Hybrid/toPost.txt'

#### User movie rating dictionary ####

userMovieRating = {}

#### Utility Functions ####

def grabCSVColumn(csv_path,columnNumber):
	import csv
	data = csv.reader(open(csv_path), delimiter="\t", quotechar='|')
	ans = []
	for row in data:
		ans.append(row[columnNumber])
	return ans

def fixTestPredictions(idsPath,toFix,toSave):
    
    ids = open(idsPath, 'r')
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
