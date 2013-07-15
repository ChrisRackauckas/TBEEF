def preProcess(os,utils,random,DE_EFFECT,userMovieRating,LAPTOP_TEST):
    
#-----------------------------------------------------------------
# Reads in data file with (userID, movieID, rating) format.
# Removes duplicates
# Randomizes the ordering
# Splits data into training_set and crossVal_set files according to
#   the specification in utils.DATA_SET_SPLIT
# De-effects
# Makes a prediction text with a "dummy" rating for libfm
# Saves in Data/PreProcessed/training_set_processed.txt
# and Data/PreProcessed/predict_dummy.txt
#-----------------------------------------------------------------

    makeDummyPredictions(utils)

    cleanUpData(utils.ORIGINAL_DATA_PATH,
                utils.ORIGINAL_DATA_CLEAN_PATH)   

    # De-effects data file
    if DE_EFFECT:
        deEffectData(utils.ORIGINAL_DATA_CLEAN_PATH, \
                 utils.PROCESSED_DATA_PATH, utils,userMovieRating)
    else:
        os.system("cp " + utils.ORIGINAL_DATA_CLEAN_PATH + " " + \
                  utils.PROCESSED_DATA_PATH)
    if LAPTOP_TEST:
        # makes a small data set able to run on laptops
        utils.bootstrap(utils.PROCESSED_DATA_PATH,\
                        utils.PROCESSED_DATA_PATH_TEMP, \
                        10000,random,False)
        os.system('mv '+utils.PROCESSED_DATA_PATH_TEMP+' '+\
                  utils.PROCESSED_DATA_PATH)

def makeDummyPredictions(utils):
#-----------------------------------------------------------------
# Makes dummy 3rd column in prediction file for LibFM
#-----------------------------------------------------------------
    inPredict = open(utils.TEST_IDS_PATH, 'r')
    outPredict = open(utils.TEST_IDS_DUMMY_PATH, 'w')
    for line in inPredict:
        if line != '\n':
            line = line.replace('\n','\t1\n') #adds dummy column
            outPredict.write(line)
    inPredict.close()
    outPredict.close()


def cleanUpData(inputPath,outputPath):
#-----------------------------------------------------------------
# Erases empty lines and duplicates, randomizes rows if randomize == True
#-----------------------------------------------------------------
    lines_seen = set() # holds lines already seen
    data = []
    newDataFile = open(outputPath,'w')
    for line in open(inputPath,'r'):
        if line != '\n':
            if line not in lines_seen: # not a duplicate
                lines_seen.add(line)
                newDataFile.write( line )
    newDataFile.close()
            
def deEffectData(infilePath, outfilePath, utils,userMovieRating):

#-----------------------------------------------------------------
# Reads in data file with (userID, movieID, rating) format.
# Saves files containing the average rating for each user, average
#   rating for each movie, and the global average rating.
# Also outputs a 'de-effected' file with format
#   (userID, movieID, newRating) where newRating is the rating
#   subtracted from the global average rating.
#-----------------------------------------------------------------

    infile = open(infilePath, 'r')
    lineCounter= 0
    usersDict = {}  # all ratings by user
    moviesDict = {} # all ratings by movie
    globalSum = 0
    umr = {} # dictionary of movies and ratings by user, saved to utils.userMovieRating
    
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
            
            if user not in umr:
                umr[user]=([movie],[rating])
            elif user in umr:
                umr[user][0].append(movie)
                umr[user][1].append(rating)
    
            
            globalSum += rating
    userMovieRating = umr       
    infile.close()

    globalMean = globalSum/lineCounter

    movieMeanDict = {}  # average rating by movie
    userMeanDict = {}   # average rating by user

    for i in usersDict:
        userMeanDict[i] = listAverager(usersDict.get(i))
        
    for i in moviesDict:
        movieMeanDict[i] = listAverager(moviesDict.get(i))

    # write de-effected data set (each rating +/- the global mean rating)
    infile = open(infilePath, 'r')
    outfile = open(outfilePath, 'w')
    for line in infile:
        line = line.replace('\n', '')
        columns = line.split('\t')
        user = columns[0]
        movie = columns[1]
        newRating = globalMean - float(columns[2])
        outfile.write(user+'\t'+movie+'\t'+ str(newRating)+'\n')
    infile.close()
    outfile.close()

    # write user effect file (average rating by user)
    userFile = open(utils.EFFECTS_USER_PATH, 'w')
    for i in userMeanDict:
        userFile.write(str(i) +'\t'+ str(userMeanDict.get(i)) + '\n')
    userFile.close()
    
    # write movie effect file (average rating by movie)
    movieFile = open(utils.EFFECTS_MOVIE_PATH, 'w')
    for i in movieMeanDict:
        movieFile.write(str(i) +'\t'+ str(movieMeanDict.get(i)) + '\n')
    movieFile.close()

    # write global effect file (global average)
    globalFile = open(utils.EFFECTS_GLOBAL_PATH, 'w')
    globalFile.write(str(globalMean))
    globalFile.close()

def listAverager(ls):

#-----------------------------------------------------------------
# Takes a list of numbers in and returns the average
#-----------------------------------------------------------------

    total = 0
    for i in ls:
        total += i
    return total/len(ls)        
