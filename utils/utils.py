#### Paths ####

TEST_IDS_PATH           = 'Data/Original/predict.txt'
TEST_IDS_DUMMY_PATH     = 'Data/PreProcessed/predict_dummy.txt'
PROCESSED_TRAIN_PATH    = 'Data/PreProcessed/training_set_processed.txt'

ORIGINAL_DATA_PATH              = 'Data/Original/data_set.txt'
ORIGINAL_DATA_CLEAN_PATH        = 'Data/PreProcessed/data_set_clean.txt'
ORIGINAL_DATA_CLEAN_RNDM_PATH   = 'Data/PreProcessed/data_set_clean_rndm.txt'
MOVIE_TAG_PATH                  = 'Data/Original/movie_tag.txt'

PROCESSED_DATA_PATH = 'Data/PreProcessed/data_set_processed.txt'

EFFECTS_USER_PATH   = 'Data/Effects/user_effects.txt'
EFFECTS_MOVIE_PATH  = 'Data/Effects/movie_effects.txt'
EFFECTS_GLOBAL_PATH = 'Data/Effects/global_effects.txt'

MODEL_BOOT_PATH       = 'Data/ModelSetup/boot_'
MODEL_RUN_PATH        = 'Data/ModelData/'
MODEL_PREDICT_PATH    = 'Data/ModelPredictions/'
MODEL_BIN_PATH        = 'Data/ModelSetup/bin_'
MODEL_FEATURED_PATH   = 'Data/ModelSetup/feat_'
MODEL_LOG_PATH        = 'Data/LogFiles/'

HYBRID_TRAIN_MATRIX_PATH    = 'Data/HybridSetup/hybridTrain.txt'
HYBRID_PREDICT_MATRIX_PATH  = 'Data/HybridSetup/hybridPredict.txt'

HYBRID_BOOT_PATH      = 'Data/HybridSetup/boot_'
HYBRID_PREDICT_PATH   = 'Data/HybridPredictions/'

HYBRID_SYNTHESIZED_PATH     = 'Data/HybridPredictions/hybridSynthesized.txt'
RE_EFFECT_PATH              = 'Data/Output/re_effect.txt' 
OUTPUT_PATH                 = 'Data/Output/output.txt'
TO_POST_PATH                = 'Data/Hybrid/toPost.txt'

#### FM ####

FM_GLOBAL_BIAS = '1' #either 1 or 0
FM_ONE_WAY_INTERACTION = '1' #either 1 or 0

#### Holds  ####

testPredictionPaths = []#Array of paths where test predictions are saved
CVPredictionPaths = []  #Array of paths where CV predictions are saved
processes = []          #Array of current processes
userMovieRating = {}    #Dictionary of user and movie ratings for de/re-effect

#### Utility Functions ####

def grabCSVColumn(csv_path,columnNumber):
	import csv
	data = csv.reader(open(csv_path,'rU'), delimiter="\t", quotechar='|')
	ans = []
	for row in data:
		ans.append(row[columnNumber])
	return ans

def prependUserMovieToPredictions(idsPath,fixPath,savePath):
    ### Takes in a column of ratings as toFix
    ### Takes in user and movie id's through idsPath
    ### Makes user movie rating and saves toSave
    ### ratingsCol is a boolean for implying
    ### whether the input for idsPath
    ### has a column of ratings or not
    import csv
    data = csv.reader(open(idsPath,'rU'), delimiter="\t", quotechar='|')
    fixData = open(fixPath, 'r')
    fixLines = fixData.readlines();
    i = 0
    output = [];
    for row in data :
        output.append(row[0] + '\t' + row[1] + "\t" + fixLines[i])
        i = i + 1
    outfile = open(savePath, 'w')
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

def randomizeData(random,inputPath,outputPath):
    lines_seen = set() # holds lines already seen
    data = [] 
    newDataFile = open(outputPath,'w')
    for line in open(inputPath,'r'):
        if line != '\n':
            if line not in lines_seen: # not a duplicate
                data.append( (random.random(), line) )
                lines_seen.add(line)
    data.sort()
    newDataFile = open(outputPath,'w')
    for _, line in data:
        newDataFile.write( line )
    newDataFile.close()

def aggregatePredictions(masterPath, foutPath, actualPred, predictionPathList):
    master = open(masterPath, 'r')
    fout = open(foutPath, 'w')
    userDict={}
    for path in predictionPathList:
        fin = open(path, 'r')
        for line in fin:
            if line != '\n':
                line = line.replace('\n','')
                columns = line.split('\t')
                user = columns[0]
                movie = columns[1]
                rating = columns[2]
                if user not in userDict:
                    userDict[user]={}
                if movie not in userDict[user]:
                    userDict[user][movie]=[]
                userDict[user][movie].append(rating)
        
    for line in master:
        if line != '\n':
            line = line.replace('\n','')
            columns = line.split('\t')
            user = columns[0]
            movie = columns[1]
            if actualPred:
                rating = columns[2]
            if user in userDict:
                if movie in userDict[user]:
                    string = ''
                    for pred in userDict[user][movie]:
                        string = string+pred+'\t'
                    string=string[:-1]  # erases the hanging tab
                    fout.write(line+'\t'+string+'\n')
            else:
                fout.write(line+'\n')
 
