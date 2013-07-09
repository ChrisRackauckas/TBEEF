def FMSetupFeatures(os,utils,model):

#-----------------------------------------------------------------
# creates the features for LibFM
#----------------------------------------------------------------- 
    if model[2] == 'Basic':
        os.system('cp ' + model[4][0] + ' ' + model[4][3])
        os.system('cp ' + model[4][1] + ' ' + model[4][4])
        os.system('cp ' + model[4][2] + ' ' + model[4][5])

#    if MOVIE_TAG:
#        print('...Movie Tag data')
#        addMovieMeta(os,utils, utils.PROCESSED_TRAIN_PATH,\
#                     utils.PROCESSED_TRAIN_TEMP_PATH)
#        addMovieMeta(os,utils, utils.PROCESSED_CV_PATH,\
#                     utils.PROCESSED_CV_TEMP_PATH)
#        addMovieMeta(os,utils, utils.TEST_IDS_DUMMY_PATH,\
#                     utils.TEST_IDS_DUMMY_TEMP_PATH)

#    if SOCIAL:
#        print('...Social data')
#        addSocialMeta(os,utils)

#   if HISTORY:
#        print('...History data')
#        addHistoryMeta(os,utils)
        

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

    os.system('mv '+foutPath+' '+ finPath)


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
    
            
 
