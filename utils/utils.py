#### Processes ####

processes = []

#### Paths ####

TEST_IDS_PATH = 'Data/Original/predict.txt'
TEST_IDS_DUMMY_PATH = 'Data/PreProcessed/predict_dummy.txt'
TEST_IDS_DUMMY_TEMP_PATH = 'Data/PreProcessed/predict_dummy_temp.txt'
PROCESSED_TRAIN_PATH = 'Data/PreProcessed/training_set_processed.txt'
PROCESSED_TRAIN_TEMP_PATH = 'Data/PreProcessed/training_set_processed_temp.txt'
PROCESSED_CV_PATH = 'Data/PreProcessed/cv_set_processed.txt'
PROCESSED_CV_TEMP_PATH = 'Data/PreProcessed/cv_set_processed_temp.txt'

ORIGINAL_DATA_PATH = 'Data/Original/data_set.txt'
ORIGINAL_DATA_NODUPS_PATH = 'Data/Original/data_set_nodups_rndm.txt'
MOVIE_TAG_PATH = 'Data/FeatureData/movie_tag.txt'

PROCESSED_DATA_PATH = 'Data/PreProcessed/data_set_processed.txt'

EFFECTS_USER_PATH = 'Data/Effects/user_effects.txt'
EFFECTS_MOVIE_PATH = 'Data/Effects/movie_effects.txt'
EFFECTS_GLOBAL_PATH = 'Data/Effects/global_effects.txt'

testPredictionPaths = [] #Array of paths where test predictions are saved
CVPredictionPaths = [] #Array of paths where CV predictions are saved

#### DATA ####

DATA_SET_SPLIT = .8 #percent of data file for training, 1-value is cross val
DATA_SIZE = 0 # value added in preprocessing

#### FM ####

FM_TRAIN_BIN_PATH = 'Data/PreProcessed/FMTrainBin'
FM_TRAIN_PATH     = 'Data/ModelData/FMTrain.txt'
FM_TEST_BIN_PATH  = 'Data/PreProcessed/FMTestBin'
FM_TEST_PATH      = 'Data/ModelData/FMTest.txt'
FM_CV_BIN_PATH    = 'Data/PreProcessed/FMCVBin'
FM_CV_PATH        = 'Data/ModelData/FMCV.txt'
FM_GLOBAL_BIAS = '1' #either 1 or 0
FM_ONE_WAY_INTERACTION = '1' #either 1 or 0
FM_PREDICTIONS_PATH = 'Data/ModelPredictions/'

#### RR ####

RR_TRAIN_PATH   = 'Data/ModelData/RRTrain.txt'
RR_TEST_PATH    = 'Data/ModelData/RRTest.txt'
RR_CV_PATH      = 'Data/ModelData/RRCV.txt'

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
	data = csv.reader(open(csv_path,'rU'), delimiter="\t", quotechar='|')
	ans = []
	for row in data:
		ans.append(row[columnNumber])
	return ans

def fixTestPredictions(idsPath,toFix,toSave):
    
    ids = open(idsPath, 'r')
    predictions = open(toFix, 'r')
    idlines = ids.readlines();
    plines = predictions.readlines();
    maxX = len(idlines)

    output = [];
    for x in range(0,maxX) :
        if x == maxX:
            output.append(idlines[x] + "\t" + plines[x])
        else :
            output.append(idlines[x][:-2] + "\t" + plines[x])
    outfile = open(toSave, 'w')
    outfile.writelines(["%s" % item  for item in output])

def prependTxtToFile(inputPath,outputPath,txt):
    with file(inputPath, 'r') as original: \
           data = original.read()
    with file(outputPath, 'w') as modified: \
           modified.write(txt + '\n' + data)


def bootstrap(inputPath, outputPath, nRows, random):
# takes nRows-many random rows with replacement from infile and writes to outfile
    fout = open(outputPath, 'w')
    rows =[]
    for line in open(inputPath, 'r'):
        rows.append(line)
    for i in range(nRows):
        fout.write(rows[ random.randint(0, len(rows)-1) ])
    fout.close()


def appendColumns(infilePath1, infilePath2, outfilePath, outputSorted):
# takes two data files and adds them together, grouping by user, sorting specified by outputSoreted
    fin1 = open(infilePath1, 'r')
    fin2 = open(infilePath2, 'r')
    fout = open(outfilePath, 'w')
    userSet = set()
    userOrder = []      # order that users appear in fin1
    linesByUser = {}    # all data lines by particular user
    for line in fin1:
        if line != '\n':
            columns = line.split('\t')
            user = int(columns[0])
            if user not in userSet:
                userSet.add(user)
                userOrder.append(user)
                linesByUser[user]=[]
            linesByUser[user].append(line)
    for line in fin2:
        if line != '\n':
            columns = line.split('\t')
            user = int(columns[0])
            if user not in userSet:
                userSet.add(user)
                userOrder.append(user)
                linesByUser[user]=[]
            linesByUser[user].append(line)
    fin1.close()
    fin2.close()
    if outputSorted:
        userOrder.sort()
    for user in userOrder:
            for line in linesByUser.get(user):
                fout.write(line)
    fout.close()
