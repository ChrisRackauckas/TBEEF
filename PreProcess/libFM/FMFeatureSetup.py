def FMSetupFeatures(os,utils,model):

#-----------------------------------------------------------------
# creates the features for LibFM
#----------------------------------------------------------------- 
    if model[2] == 'Basic':
        # sends bootTrain, bootCV, bootTest to featTrain, featCv, featTest
        os.system('cp ' + model[4][0] + ' ' + model[4][3])
        os.system('cp ' + model[4][1] + ' ' + model[4][4])
        os.system('cp ' + model[4][2] + ' ' + model[4][5])

    if model[2] == 'MovieTag':
        print('...Movie Tag data')
        addMovieMeta(os,utils, model[4][0], model[4][3] )
        addMovieMeta(os,utils, model[4][1], model[4][4] )
        addMovieMeta(os,utils, model[4][2], model[4][5] )

    if model[2] == 'NearestNeighbor':
        print('...Nearest Neighbor data')
        nearestNeighbor(os,utils, model[4][0], model[4][3] )
        nearestNeighbor(os,utils, model[4][1], model[4][4] )
        nearestNeighbor(os,utils, model[4][2], model[4][5] )
        
    if model[2] == 'Social':
        # TODO
        print('...Social data')
        addSocialMeta(os,utils, model[4][0], model[4][3] )
        addSocialMeta(os,utils, model[4][1], model[4][4] )
        addSocialMeta(os,utils, model[4][2], model[4][5] )

    if model[2] == 'History':
        # TODO
        print('...History data')
        addHistoryMeta(os,utils, model[4][0], model[4][3] )
        addHistoryMeta(os,utils, model[4][1], model[4][4] )
        addHistoryMeta(os,utils, model[4][2], model[4][5] )
        

def addMovieMeta(os, utils, finPath, foutPath):

#-----------------------------------------------------------------
# creates new data set with movie tag feature for LibFM
#-----------------------------------------------------------------

    movieTags = open(utils.MOVIE_TAG_PATH, 'r')
    tagDict = {}
    for line in movieTags:
        if line != '\n':
            line = line.replace('\n', '')
            columns = line.split('\t')
            movie = columns[0]
            allTags = columns[1]
            allTags = allTags.replace(',', '\t')
            tagDict[movie]=allTags
    dataSet = open(finPath,'r')
    dataSetWithTags = open(foutPath,'w')
    for line in dataSet:
        if line != '\n':
            line = line.replace('\n', '')
            columns = line.split('\t')
            movie = columns[1]
            if movie in tagDict:
                dataSetWithTags.write(line+'\t'+tagDict.get(movie)+'\n')
            else:
                dataSetWithTags.write(line+'\n')

    movieTags.close()
    dataSet.close()
    dataSetWithTags.close()


def nearestNeighbor(os, utils, fin, fout):

#-----------------------------------------------------------------
# creates new data set with NN data for LibFM
#-----------------------------------------------------------------

    # TODO
    return

    
def addSocialMeta(os,utils):

#-----------------------------------------------------------------
# creates new data set with social feature for LibFM
#-----------------------------------------------------------------

    # TODO
    return


def addHistoryMeta(os,utils):

#-----------------------------------------------------------------
# creates new data set with user history feature for LibFM
#-----------------------------------------------------------------

    # TODO
    return
    
            
 
