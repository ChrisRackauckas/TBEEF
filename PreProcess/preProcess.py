def preProcess(os,utils):

#-----------------------------------------------------------------
# Reads in data file with (userID, movieID, rating) format.
# Removes duplicates
# Randomizes the ordering
# De-effects
# Makes a prediction text with a "dummy" rating
# Saves in Data/PreProcessed/training_set_processed.txt
# and Data/PreProcessed/predict_dummy.txt
#-----------------------------------------------------------------



def deEffectData(infilePath, outfilePath):

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
    

    return userMeanDict, movieMeanDict, globalMean


def listAverager(ls):
    total = 0
    for i in ls:
        total += i
    return total/len(ls)
        
        
