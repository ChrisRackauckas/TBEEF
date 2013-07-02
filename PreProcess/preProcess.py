def preProcess(os,utils,random):
    
#-----------------------------------------------------------------
# Reads in data file with (userID, movieID, rating) format.
# Removes duplicates
# Randomizes the ordering
# Splits data into training_set and crossVal_set files according to
#   the specification in utils.DATA_SET_SPLIT
# De-effects
# Makes a prediction text with a "dummy" rating
# Saves in Data/PreProcessed/training_set_processed.txt
# and Data/PreProcessed/predict_dummy.txt
#-----------------------------------------------------------------

    # makes dummy prediction file
    print("Preprocessing data...")
    inPredict = open(utils.TEST_IDS_PATH, 'r')
    outPredict = open(utils.TEST_IDS_DUMMY_PATH, 'w')
    for line in inPredict:
        if line != '\n':
            line = line.replace('\n', '\t1\n') #adds dummy column
            outPredict.write(line)

    
    # randomizes, no dups
    lines_seen = set() # holds lines already seen
    data = []
    for line in open(utils.ORIGINAL_DATA_PATH,'r'):
        if line != '\n':
            if line not in lines_seen: # not a duplicate
                data.append( (random.random(), line) )
                lines_seen.add(line)
    data.sort()
    lenData = len(data)
    newDataFile = open(utils.ORIGINAL_DATA_RNDM_NODUPS_PATH,'w')
    for _, line in data:
        newDataFile.write( line )
            

    # De-effects data file
    deEffectData(utils.ORIGINAL_DATA_RNDM_NODUPS_PATH, \
                 utils.PROCESSED_DATA_PATH, utils)

    # Splits data set
    splitData(utils, lenData)


def splitData(utils, lineCount):
    counter = 0
    data = open(utils.PROCESSED_DATA_PATH, 'r')
    training = open(utils.PROCESSED_TRAIN_PATH, 'w')
    crossVal = open(utils.PROCESSED_CROSSVAL_PATH, 'w')
    for line in data:
        if counter < int(lineCount * utils.DATA_SET_SPLIT):
            training.write( line )
            counter +=1
        else:
            crossVal.write( line )

    

def deEffectData(infilePath, outfilePath, utils):

#-----------------------------------------------------------------
# Reads in data file with (userID, movieID, rating) format.
# Returns dictionaries of average rating for each user, average
#   rating for each movie, and the global average rating.
# Output txt file with format (userID, movieID, newRating) where
#   newRating has been subtracted from the global average rating.
#-----------------------------------------------------------------

    infile = open(infilePath, 'r')
    #initialize variables
    lineCounter= 0
    usersDict = {}
    moviesDict = {}
    globalSum = 0
    
    for line in infile:
        if line != '\n':
            lineCounter += 1
            line = line.replace('\n', '')
            columns = line.split('\t')
            user = columns[0]
            movie = columns[1]
            rating = float(columns[2])

            if usersDict.get(user)==None:
                usersDict[user]=[]
            usersDict[user].append(rating)

            if moviesDict.get(movie)==None:
                 moviesDict[movie]=[]
            moviesDict[movie].append(rating)

            globalSum += rating
            
    infile.close()

    globalMean = globalSum/lineCounter

    movieMeanDict = {}
    userMeanDict = {}

    for i in usersDict:
        userMeanDict[i] = listAverager(usersDict.get(i))
        
    for i in moviesDict:
        movieMeanDict[i] = listAverager(moviesDict.get(i))

    # write to file data set +/- the global mean rating
    infile = open(infilePath, 'r')
    outfile = open(outfilePath, 'w')
    for line in infile:
        line = line.replace('\n', '')
        columns = line.split('\t')
        user = columns[0]
        movie = columns[1]
        newRating = globalMean - float(columns[2])
        outfile.write(user+'\t'+movie+'\t'+ str(newRating)+'\n')

    # write user effect file
    userFile = open(utils.EFFECTS_USER_PATH, 'w')
    for i in userMeanDict:
        userFile.write(str(i) +'\t'+ str(userMeanDict.get(i)) + '\n')
    
    # write movie effect file
    movieFile = open(utils.EFFECTS_MOVIE_PATH, 'w')
    for i in movieMeanDict:
        movieFile.write(str(i) +'\t'+ str(movieMeanDict.get(i)) + '\n')

    # write global effect file
    globalFile = open(utils.EFFECTS_GLOBAL_PATH, 'w')
    globalFile.write(str(globalMean))

        

def listAverager(ls):
    total = 0
    for i in ls:
        total += i
    return total/len(ls)
        
        
