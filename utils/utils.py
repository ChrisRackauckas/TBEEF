#### Paths ####

TEST_IDS_PATH = 'Data/Original/predict.txt'
TEST_IDS_DUMMY_PATH = 'Data/PreProcessed/predict_dummy.txt'
PROCESSED_TRAIN_PATH = 'Data/PreProcessed/training_set_processed.txt'

ORIGINAL_DATA_PATH = 'Data/Original/data_set.txt'
ORIGINAL_DATA_CLEAN_PATH = 'Data/PreProcessed/data_set_clean.txt'

MOVIE_TAG_PATH = 'Data/Original/movie_tag.txt'
USER_SOCIAL_PATH = 'Data/Original/user_social.txt'
USER_HISTORY_PATH = 'Data/Original/user_history.txt'

PROCESSED_SOCIAL = 'Data/PreProcessed/processed_social.txt'
PROCESSED_HISTORY = 'Data/PreProcessed/processed_history.txt'
PROCESSED_MOVIE_TAGS = 'Data/PreProcessed/processed_movie_tag.txt'

PROCESSED_DATA_PATH = 'Data/PreProcessed/data_set_processed'
PROCESSED_DATA_PATH_TEMP = 'Data/PreProcessed/data_set_processed_temp'

EFFECTS_USER_PATH = 'Data/Effects/user_effects.txt'
EFFECTS_MOVIE_PATH = 'Data/Effects/movie_effects.txt'
EFFECTS_GLOBAL_PATH = 'Data/Effects/global_effects.txt'

MODEL_BOOT_PATH = 'Data/ModelSetup/boot_'
MODEL_RUN_PATH = 'Data/ModelData/'
MODEL_PREDICT_PATH = 'Data/ModelPredictions/'
MODEL_TMP_PATH = 'Data/ModelSetup/tmp_'
MODEL_FEATURED_PATH = 'Data/ModelSetup/feat_'
MODEL_LOG_PATH = 'Data/LogFiles/'
MODEL_CONFIG_PATH = 'Data/ModelData/cfg_'

HYBRID_ORIGINAL_PATH = 'Data/HybridSetup/orig_'
HYBRID_BOOT_PATH = 'Data/HybridSetup/boot_'
HYBRID_LOG_PATH = 'Data/LogFiles/h_'
HYBRID_PREDICT_PATH = 'Data/HybridPredictions/'
HYBRID_RMSE_PATH = 'Data/HybridPredictions/RMSE_'

SYNTH_ORIGINAL_PATH = 'Data/SynthSetup/orig_'
SYNTH_BOOT_PATH = 'Data/SynthSetup/boot_'
SYNTH_PREDICT_PATH = 'Data/SynthPredictions/'
SYNTH_RMSE_PATH = 'Data/SynthPredictions/RMSE_'
SYNTH_LOG_PATH = 'Data/LogFiles/s_'

TRIAL_OUTPUT_PATH = 'Data/Output/'
OUTPUT_PATH = 'Data/Output/output.txt'

#### FM ####

FM_GLOBAL_BIAS = '1' #either 1 or 0
FM_ONE_WAY_INTERACTION = '1' #either 1 or 0
LIBFM_BINARY = './Models/libFM/libFM'

#### SVD Feature ###

SVDFEATURE_BUFFER_BINARY    = './Models/SVDFeature/tools/make_feature_buffer'
SVDFEATURE_GROUP_BUFFER_BINARY = './Models/SVDFeature/tools/make_ugroup_buffer'
SVDFEATURE_LINE_REORDER     = './Models/SVDFeature/tools/line_reorder'
SVDFEATURE_SVDPP_RANDORDER  = './Models/SVDFeature/tools/svdpp_randorder'
SVDFEATURE_BINARY           = './Models/SVDFeature/svd_feature'
SVDFEATURE_INFER_BINARY     = './Models/SVDFeature/svd_feature_infer'
SVDFEATURE_MODEL_OUT_PATH   = 'Data/ModelData/'

#### Utility Functions ####

def grabCSVColumn(csv_path, columnNumber):
    import csv

    data = csv.reader(open(csv_path, 'rU'), delimiter="\t", quotechar='|')
    ans = []
    for row in data:
        ans.append(row[columnNumber])
    return ans


def prependTxtToFile(inputPath, outputPath, txt):
    with file(inputPath, 'r') as original:
        data = original.read()
    with file(outputPath, 'w') as modified:
        modified.write(txt + '\n' + data)


def bootstrap(inputPath, outputPath, nRows, random, replace):
# takes nRows-many random rows 
# with/wihout replacement (boolean replace)
# from infile and writes to outfile
    fout = open(outputPath, 'w')
    rows = []
    fin = open(inputPath, 'r')
    if replace:
        for line in fin:
            rows.append(line)
        for i in range(nRows):
            fout.write(rows[random.randint(0, len(rows) - 1)])
    else:
        finLines = fin.readlines()
        samples = random.sample(range(0, len(finLines)), nRows)
        for i in samples:
            rows.append(finLines[i])
        for row in rows:
            fout.write(row)
    fout.close()


def bootsplit(inputPath, tempPath, outputPath1, outputPath2, split, random):
    #Takes in an input data
    #Randomizes it and splits it
    #Same as sampling without replacement
    #And saving leftovers as a second dataset
    randomizeData(random, inputPath, tempPath)
    splitData(tempPath, outputPath1, outputPath2, split)


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
                linesByUser[user] = []
            linesByUser[user].append(line)
    for line in fin2:
        if line != '\n':
            columns = line.split('\t')
            user = int(columns[0])
            if user not in userSet:
                userSet.add(user)
                userOrder.append(user)
                linesByUser[user] = []
            linesByUser[user].append(line)
    fin1.close()
    fin2.close()
    if outputSorted:
        userOrder.sort()
    for user in userOrder:
        for line in linesByUser.get(user):
            fout.write(line)
    fout.close()


def randomizeData(random, inputPath, outputPath):
    lines_seen = set() # holds lines already seen
    data = []
    newDataFile = open(outputPath, 'w')
    for line in open(inputPath, 'r'):
        if line != '\n':
            if line not in lines_seen: # not a duplicate
                data.append((random.random(), line))
                lines_seen.add(line)
    data.sort()
    newDataFile = open(outputPath, 'w')
    for _, line in data:
        newDataFile.write(line)
    newDataFile.close()


def aggregatePredictions(masterPath, foutPath, actualPred, predictionPathList):
    master = open(masterPath, 'r')
    fout = open(foutPath, 'w')
    userDict = {}
    for path in predictionPathList:
        fin = open(path, 'r')
        for line in fin:
            if line != '\n':
                line = line.replace('\n', '')
                columns = line.split('\t')
                user = columns[0]
                movie = columns[1]
                rating = columns[2]
                if user not in userDict:
                    userDict[user] = {}
                if movie not in userDict[user]:
                    userDict[user][movie] = []
                userDict[user][movie].append(rating)

    for line in master:
        if line != '\n':
            line = line.replace('\n', '')
            columns = line.split('\t')
            user = columns[0]
            movie = columns[1]
            if actualPred:
                rating = columns[2]
            if user in userDict:
                if movie in userDict[user]:
                    string = ''
                    for pred in userDict[user][movie]:
                        string = string + pred + '\t'
                    string = string[:-1]  # erases the hanging tab
                    fout.write(line + '\t' + string + '\n')
            else:
                fout.write(line + '\n')


def splitData(inputPath, outputPath1, outputPath2, split):
#-----------------------------------------------------------------
# Takes the processed data file and splits it into a training set
#   and cross validation set according to utils.DATA_SET_SPLIT
#-----------------------------------------------------------------
    counter = 0
    data = open(inputPath, 'r')
    outfile1 = open(outputPath1, 'w')
    outfile2 = open(outputPath2, 'w')
    dataLines = data.readlines()
    lineCount = len(dataLines)
    for line in dataLines:
        if counter < int(lineCount * split):
            outfile1.write(line)
            counter += 1
        else:
            outfile2.write(line)
    data.close()
    outfile1.close()
    outfile2.close()
