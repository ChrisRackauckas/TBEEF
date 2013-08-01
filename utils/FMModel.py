from Model import Model
class FMModel(Model):

################################
######### Constructors #########
    
    def __init__(self,configModel,utils,config,strTrial):
        super(FMModel,self).__init__(configModel,utils,strTrial)
        self.dims = configModel[3][0]
        self.logCV          = utils.MODEL_LOG_PATH      + self.tag + \
                                      '_CV' + '_t' + strTrial
        self.logTest        = utils.MODEL_LOG_PATH      + self.tag + \
                                    '_test' + '_t' + strTrial
        self.libFMBinary            = utils.LIBFM_BINARY
        self.strItr                 = config.FM_STR_ITER
        self.globalBias             = utils.FM_GLOBAL_BIAS
        self.oneWay                 = utils.FM_ONE_WAY_INTERACTION
        self.initStd                = config.FM_INIT_STD
        
        self.cleanData              = utils.ORIGINAL_DATA_CLEAN_PATH
        self.movieTag               = utils.MOVIE_TAG_PATH
        self.historyTag             = utils.PROCESSED_HISTORY
        self.social                 = utils.PROCESSED_SOCIAL
        self.sharedTag              = utils.PROCESSED_MOVIE_TAGS
        self.meanMovieRating        = utils.EFFECTS_MOVIE_PATH

##################################
########### Setup Data ###########

    def setup(self):
        ### Take boot to feat ###
        print("Setting Up Features")
        self.setupFeatures()
        ### Take feat to bin to run ###
        print("Converting Data")
        self.dataConvert()

    def libFMFormat(self, targetCol):
        #-----------------------------
        # Takes in raw data from original
        # Then formats it into sparse .libfm matrix
        #-----------------------------
        import os
        os.system('perl Models/libFM/triple_format_to_libfm.pl -in ' + 
            self.featTrain  + ',' +  
            self.featCV + ',' +
            self.featTest +
            ' -target '+str(targetCol)+' -separator \"\\t\"')
        
    def dataConvert(self):
        import os
        #-----------------------------
        # Takes in the .libfm sparse matrix
        # Then converts it to the binary form
        #-----------------------------
        
        os.sys.stdout.write('{0}\r'.format('-- Converting (1/6) ' + self.tag + ' --') )
        os.system('./Models/libFM/convert --ifile ' + 
            self.featTrain + 
            '.libfm ' + '--ofilex ' + 
            self.tmpTrain + 
            '.x --ofiley ' + 
            self.runTrain + '.y' +
            '> /dev/null')
        os.sys.stdout.write('{0}\r'.format('-- Converting (2/6) ' + self.tag + ' --') )
        os.system('./Models/libFM/convert --ifile ' + 
            self.featCV + 
            '.libfm ' + '--ofilex ' + 
            self.tmpCV +
            '.x --ofiley ' + 
            self.runCV + '.y' +
            '> /dev/null')
        os.sys.stdout.write('{0}\r'.format('-- Converting (3/6) ' + self.tag + ' --') )
        os.system('./Models/libFM/convert --ifile ' + 
            self.featTest + 
            '.libfm ' + '--ofilex ' + 
            self.tmpTest + 
            '.x --ofiley ' + 
            self.runTest + '.y'
            '> /dev/null')
        os.sys.stdout.write('{0}\r'.format('-- Converting (4/6) ' + self.tag + ' --') )
        os.system('./Models/libFM/transpose --ifile ' + 
            self.tmpTrain + 
            '.x --ofile ' + 
            self.runTrain + '.xt' +
            '> /dev/null')
        os.sys.stdout.write('{0}\r'.format('-- Converting (5/6) ' + self.tag + ' --') )
        os.system('./Models/libFM/transpose --ifile ' + 
            self.tmpCV + '.x --ofile ' + 
            self.runCV + '.xt' + 
            '> /dev/null')
        os.sys.stdout.write('{0}\r'.format('-- Converting (6/6) ' + self.tag + ' --') )
        os.system('./Models/libFM/transpose --ifile ' + 
            self.tmpTest + 
            '.x --ofile ' + 
            self.runTest + '.xt' +
            '> /dev/null')
        print(self.tag + ' data is converted.')

#########################################
########### Develop Features ############

    def setupFeatures(self):
        import os
        #-----------------------------------------------------------------
        # creates the features for LibFM, then turns into sparse matrix
        #----------------------------------------------------------------- 

        # ---- ---- Basic Features ---- ---- #

        if self.featureSet == 'Basic':
            os.system('cp ' + self.bootTrain + ' ' + self.featTrain)
            os.system('cp ' + self.bootCV    + ' ' + self.featCV   )
            os.system('cp ' + self.bootTest  + ' ' + self.featTest )
            self.libFMFormat(2)

        elif self.featureSet == 'NearestNeighbor':  
            print('...Adding Nearest Neighbor Data')
            moviesRatedByUserDict = self.moviesRatedByUserDict()
            movieLocationDict = self.userMovieLocationDict(False,True)
        
            self.addNearestNeighbor(self.bootTrain,self.featTrain,moviesRatedByUserDict,movieLocationDict,'train')
            self.addNearestNeighbor(self.bootCV,self.featCV,moviesRatedByUserDict,movieLocationDict,'CV')
            self.addNearestNeighbor(self.bootTest,self.featTest,moviesRatedByUserDict,movieLocationDict,'test')

        ### Baidu Dataset Specific Features ###

        # ---- ---- Movie Tag Features ---- ---- #

        elif self.featureSet == 'BasicMovieTag':
            print('...Adding Basic Movie Tag Data')
            tagDict = self.movieTagDict()
            
            self.basicMovieTag(self.bootTrain,self.featTrain,tagDict,'train')
            self.basicMovieTag(self.bootCV,self.featCV,tagDict,'CV')
            self.basicMovieTag(self.bootTest,self.featTest,tagDict,'test')
            self.libFMFormat(2)

        elif self.featureSet == 'RelatedMovieTagThreshold':
            print('...Adding Related Movie Tag Threshold Data')
            threshold = 6
            movieSharedTagDict, maxTags = self.movieSharedTagDict(threshold) 
            userLocationDict, movieLocationDict = self.userMovieLocationDict(True,True)
            
            self.relatedMovieTagThreshold(self.bootTrain,self.featTrain, movieSharedTagDict, maxTags, userLocationDict, movieLocationDict,threshold,'train')
            self.relatedMovieTagThreshold(self.bootCV,self.featCV, movieSharedTagDict, maxTags, userLocationDict, movieLocationDict,threshold,'CV')
            self.relatedMovieTagThreshold(self.bootTest,self.featTest, movieSharedTagDict, maxTags, userLocationDict, movieLocationDict,threshold,'test')

        elif self.featureSet == 'RelatedMovieTagThreshold2':
            print('...Adding Related Movie Tag Threshold 2 Data')
            threshold = 6
            movieSharedTagDict, maxTags = self.movieSharedTagDict(threshold)
            userLocationDict, movieLocationDict = self.userMovieLocationDict(True,True)
            moviesRatedByUserDict = self.moviesRatedByUserDict()
            
            self.relatedMovieTagThreshold2(self.bootTrain,self.featTrain, movieSharedTagDict, maxTags, userLocationDict, movieLocationDict,moviesRatedByUserDict,'train')
            self.relatedMovieTagThreshold2(self.bootCV,self.featCV, movieSharedTagDict, maxTags, userLocationDict, movieLocationDict,moviesRatedByUserDict,'CV')
            self.relatedMovieTagThreshold2(self.bootTest,self.featTest, movieSharedTagDict, maxTags, userLocationDict, movieLocationDict,moviesRatedByUserDict,'test')

        # ---- ---- User History Features ---- ---- #

        elif self.featureSet == 'UserHistory':   
            print('...Adding User History Data')
            moviesRatedByUserDict = self.moviesRatedByUserDict()
            userHistoryDict = self.userHistoryDict()
            movieLocationDict = self.userMovieLocationDict(False,True)
        
            self.userHistory(self.bootTrain,self.featTrain,userHistoryDict,movieLocationDict,moviesRatedByUserDict,'train')
            self.userHistory(self.bootCV,self.featCV,userHistoryDict,movieLocationDict,moviesRatedByUserDict,'CV')
            self.userHistory(self.bootTest,self.featTest,userHistoryDict,movieLocationDict,moviesRatedByUserDict,'test')

        # ---- ---- User Social Features ---- ---- #

        elif self.featureSet == 'UserSocial':
            print('...Adding User Social Data')
            userLocationDict, movieLocationDict = self.userMovieLocationDict(True,True)
            userSocialDict = self.userSocialDictReader()
            
            self.userSocial(self.bootTrain,self.featTrain,userLocationDict,movieLocationDict,userSocialDict,'train')
            self.userSocial(self.bootCV,self.featCV,userLocationDict,movieLocationDict,userSocialDict,'CV')
            self.userSocial(self.bootTest,self.featTest,userLocationDict,movieLocationDict,userSocialDict,'test')

        ### End Baidu Dataset Specific Features ###

    def addNearestNeighbor(self,finPath, foutPath,moviesRatedByUserDict,movieLocationDict,step):
        #-----------------------------------------------------------------
        # creates sparse matrix where non-user/movie entries given as column:rating/m
        # where m is the total number of movies rated by the user
        #-----------------------------------------------------------------

        lineCount= self.lineCount(finPath)
        counter = 0

        offset = len(movieLocationDict)
        fin = open(finPath, 'r')
        fout = open(foutPath + '.libfm', 'w')
        for line in fin:
            line.replace('\n', '')
            columns = line.split('\t')
            user = columns[0]
            movie = columns[1]
            rating = columns[2]
            movCol = movieLocationDict[movie]
            string=''   
            m = len(moviesRatedByUserDict[user])    # num of movies rated by user
            for mov in moviesRatedByUserDict[user]:
                rate = moviesRatedByUserDict[user][mov]    # other movie's rating
                location = str( int(movieLocationDict[mov]) + offset )
                val = str( '{0:.4f}'.format( float(rate)/m ) ) # r/m
                string = string + location+':'+val+' '
            string=string[:-1]  # gets rid of the extra space on the end
            fout.write(rating[:-1]+' '+movCol+':1 '+string+'\n')

            self.printProgress(counter, lineCount,step)
            counter +=1
        self.printProgressDone(step)
        fin.close()
        fout.close()

    def basicMovieTag(self,finPath, foutPath, tagDict,step):
        #-----------------------------------------------------------------
        # creates new data set with movie tag info by appending tags as columns
        # Output data still needs to by formatted for LibFM
        #-----------------------------------------------------------------

        lineCount= self.lineCount(finPath)
        counter=0
        
        dataSet = open(finPath,'r')
        dataSetWithTags = open(foutPath,'w')
        for line in dataSet:
            if line != '\n':
                line = line.replace('\n', '')
                columns = line.split('\t')
                movie = columns[1]
                if movie in tagDict:
                    string =''
                    for tag in tagDict[movie]:
                        string=string+tag+'\t'
                    string[:-1] # gets rid of extra tab on end
                    dataSetWithTags.write(line+'\t'+string+'\n')
                else:
                    dataSetWithTags.write(line+'\n')

                self.printProgress(counter, lineCount,step)
                counter +=1
        self.printProgressDone(step)
        dataSet.close()
        dataSetWithTags.close()

    def relatedMovieTagThreshold(self,finPath, foutPath, movieSharedTagDict, maxTags, userLocationDict, movieLocationDict, threshold,step):
        #-----------------------------------------------------------------
        # creates sparse matrix using movie tags with userID, movieID, then columns
        #  with movies that share at least n tags are given a (n-t)/max value, max
        #  is most tags shared between any given pair
        #-----------------------------------------------------------------

        lineCount= self.lineCount(finPath)
        counter=0

        offset = len(movieLocationDict)
        dataSet = open(finPath,'r')
        fout = open(foutPath + '.libfm','w')
        for line in dataSet:
            if line != '\n':
                line = line.replace('\n', '')
                columns = line.split('\t')
                user=columns[0]
                movie = columns[1]
                rating= columns[2]
                movCol = movieLocationDict[movie]
                userCol = userLocationDict[user]
                if movie in movieSharedTagDict:
                    string=''
                    for tup in movieSharedTagDict[movie]:
                        mov2 = tup[0]
                        if mov2 in movieLocationDict: # some movies in tag data are not in training set
                            num = tup[1]
                            val = str( '{0:.4f}'.format( (num-threshold+1)/maxTags ) ) # value
                            loc = int(movieLocationDict[mov2])+offset
                            string=string+str(loc)+':'+val+' '
                    string=string[:-1]
                    fout.write(rating+' '+userCol+':1 '+movCol+':1 '+string+'\n')
                else:
                    fout.write(rating+' '+userCol+':1 '+movCol+':1\n')
                self.printProgress(counter, lineCount, step)
                counter +=1
        self.printProgressDone(step)
        dataSet.close()
        fout.close()

    def relatedMovieTagThreshold2(self,finPath, foutPath, movieSharedTagDict, maxTags, userLocationDict, movieLocationDict,moviesRatedByUserDict,step):
        #-----------------------------------------------------------------
        # creates sparse matrix using movie tags with userID, movieID, then columns
        #  with movies that share at least n tags and have been rated by same user are assigned a value of
        #  (n/maxTags + rating/m), m is total number of movies rated by user; otherwise val is just n/maxTags
        #-----------------------------------------------------------------

        lineCount= self.lineCount(finPath)
        counter=0

        offset = len(movieLocationDict)
        dataSet = open(finPath,'r')
        fout = open(foutPath + '.libfm','w')
        for line in dataSet:
            if line != '\n':
                line = line.replace('\n', '')
                columns = line.split('\t')
                user=columns[0]
                movie = columns[1]
                rating= columns[2]
                movCol = movieLocationDict[movie]
                userCol = userLocationDict[user]
                if movie in movieSharedTagDict and movie in movieLocationDict:
                    string=''
                    for tup in movieSharedTagDict[movie]:
                        mov2 = tup[0]
                        numTags = tup[1]
                        if mov2 in movieLocationDict:
                            if mov2 in moviesRatedByUserDict[user]:
                                r2 = moviesRatedByUserDict[user][mov2]     # user rating of mov2
                                m = len(moviesRatedByUserDict[user])
                                val = str( '{0:.4f}'.format( (numTags/maxTags)+(float(r2)/m) )) # value
                            else:
                                val = str( '{0:.4f}'.format( numTags/maxTags) ) # value
                            loc = int(movieLocationDict[mov2])+offset
                            string=string+str(loc)+':'+val+' '
                    string=string[:-1]
                    fout.write(rating+' '+userCol+':1 '+movCol+':1 '+string+'\n')
                else:
                    fout.write(rating+' '+userCol+':1 '+movCol+':1\n')

                self.printProgress(counter, lineCount, step)
                counter +=1
        self.printProgressDone(step)
        dataSet.close()
        fout.close()

    def userHistory(self,finPath, foutPath,userHistoryDict,movieLocationDict,moviesRatedByUserDict,step):
        #-----------------------------------------------------------------
        # creates sparse matrix using user history using movieID,
        #  then rating/n for each movie in user history and rated, where n is total viewed
        #  and simply 1/n for each movie in history and unrated by user
        #-----------------------------------------------------------------

        lineCount= self.lineCount(finPath)
        counter=0

        offset = len(movieLocationDict)
        fin = open(finPath, 'r')
        fout = open(foutPath + '.libfm', 'w')
        for line in fin:
            line.replace('\n', '')
            columns = line.split('\t')
            user = columns[0]
            movie = columns[1]
            rating = columns[2]
            movCol = movieLocationDict[movie]
            string=''   
            n = max(len(moviesRatedByUserDict[user]), len(userHistoryDict[user]) )   
            for mov in userHistoryDict[user]:
                if mov in moviesRatedByUserDict[user]:
                    rate = float(moviesRatedByUserDict[user][mov])
                else:
                    rate = 1
                location = str( int(movieLocationDict[mov]) + offset )
                val = str( '{0:.4f}'.format( rate/n ) ) 
                string = string + location+':'+val+' '
            string=string[:-1]  # gets rid of the extra space on the end
            fout.write(rating[:-1]+' '+movCol+':1 '+string+'\n')

            self.printProgress(counter, lineCount, step)
            counter +=1
        self.printProgressDone(step)
        fin.close()
        fout.close()

    def userSocial(self,finPath,foutPath,userLocationDict,movieLocationDict,userSocialDict,step):
        #-----------------------------------------------------------------
        # creates sparse matrix using user social data 
        #-----------------------------------------------------------------

        lineCount= self.lineCount(finPath)
        counter=0

        offset = len(movieLocationDict)+len(userLocationDict)
        fin = open(finPath,'r')
        fout = open(foutPath + '.libfm','w')
        for line in fin:
            if line != '\n':
                line = line.replace('\n', '')
                columns = line.split('\t')
                user=columns[0]
                movie = columns[1]
                rating= columns[2]
                movCol = movieLocationDict[movie]
                userCol = userLocationDict[user]
                string = ''
                if user in userSocialDict:
                    m = len(userSocialDict[user])  # num of friends
                    val = str( '{0:.4f}'.format( 1/m ) )
                    for friend in userSocialDict[user]:
                        loc = str( int(userLocationDict[friend])+offset )
                        string = string + loc +':'+ val +' '
                    string=string[:-1]
                fout.write(rating+' '+userCol+':1 '+movCol+':1 '+string+'\n')

                self.printProgress(counter, lineCount, step)
                counter +=1
        self.printProgressDone(step)
        fin.close()
        fout.close()

#######################################
########## Helpful Functions ##########

    def lineCount(self,finPath):
        # returns a line count on the input file
        fin = open(finPath, 'r')    
        lineCount=0
        for line in fin:
            lineCount+=1
        fin.close()
        return lineCount

    def printProgress(self, counter, lineCount, step):
        # prints to system how much of data has been formatted
        printEvery = int(lineCount*0.05)
        if printEvery < 1:
            printEvery=1
        if counter%printEvery==0:
            print('{0}\r'.format( str('-- '+str('{0:.2f}'.format(counter/lineCount*100))+ ' percent of data formatted for ' + self.tag + ' Trial: ' + self.trial + ' Step: ' + step )) )

    def printProgressDone(self, step):
        # prints to system that formatting is completed
        print('{0}\r'.format('-- Formatting Complete For ' + self.tag + ' Trial: ' + self.trial + ' Step: ' + step)) # space included on purpose to overwrite previous string
        print() # to move to nextline

##################################################
########## Dictionary Reading Functions ##########

    def userMovieLocationDict(self, user,movie):
        # returns two dicts, one with users as keys and the other with movies as keys. Both hold location in sparse matrix as value
        location = 1
        if user: # first time through we get user locations
            dataSet=open(self.cleanData, 'r')
            userLocationDict={}
            userSet=set()
            for line in dataSet:
                columns = line.split('\t')
                user = columns[0]
                if user not in userSet:
                    userSet.add(user)
                    userLocationDict[user]= str(location)
                    location += 1
            dataSet.close()
        if movie:   # this time get movie locations
            dataSet=open(self.cleanData, 'r')
            movieLocationDict={}
            movieSet=set()
            for line in dataSet:
                columns = line.split('\t')
                movie = columns[1]
                if movie not in movieSet:
                    movieSet.add(movie)
                    movieLocationDict[movie] = str(location)
                    location +=1
            dataSet.close()
        if user and not movie: # means movie is False
            return userLocationDict
        elif not user and movie: # means user is False
            return movieLocationDict
        else:
            return userLocationDict, movieLocationDict # otherwise we want both (even if false, false)


    def movieTagDict(self):
        # returns a dict with movies as keys and list of tags as value
        movieTags = open(self.movieTag, 'r')
        tagDict = {}
        for line in movieTags:
            if line != '\n':
                line = line.replace('\n', '')
                columns = line.split('\t')
                movie = columns[0]
                allTags = columns[1]
                tagList = allTags.split(',')
                tagDict[movie]=[]
                for tag in tagList:
                    tagDict[movie].append(tag)
        return tagDict

    def movieSharedTagDict(self, threshold):
        # returns a dict with movies as keys and list of (movie, num shared tag) tuples
        #  where threshold cuts out any movie pairs that do not share at least $threshold many tags
        sharedTags = open(self.sharedTag, 'r')
        maxTag = 0  # max number of shared tags between all movie pairs
        movieSet = set()
        tagDict = {}
        for line in sharedTags:
            if line != '\n':
                line = line.replace('\n', '')
                columns = line.split('\t')
                movie1 = columns[0]
                movie2 = columns[1]
                numTags = int(columns[2])
                if numTags >= threshold:
                    if numTags > maxTag:
                        maxTag = numTags
                    if movie1 not in movieSet:
                        tagDict[movie1]=[]
                        movieSet.add(movie1)
                    tagDict[movie1].append( (movie2, numTags) ) # movie2 is a string ID, numTags is an int
        return tagDict, maxTag

    def movieTagAndLocationDict(self,startVal):
        # returns two dicts, one of tags by movie, the other
        #  of movieTag locations, where first location is at StartVal
        movieTags = open(self.movieTag, 'r')
        tagDict = {}
        tagLocationDict={}
        tagSet=set()
        location = startVal
        for line in movieTags:
            if line != '\n':
                line = line.replace('\n', '')
                columns = line.split('\t')
                movie = columns[0]
                allTags = columns[1]
                tagList = allTags.split(',')
                tagDict[movie]=[]
                for tag in tagList:
                    tagDict[movie].append(tag)
                    if tag not in tagSet:
                        tagLocationDict[tag]=str(location)
                        location += 1
        return tagDict, tagLocationDict

    def moviesRatedByUserDict(self):
        # returns a dict of dicts with user as keys and a dict of movie:rating as values
        userSet=set()   
        moviesRatedByUserDict = {}
        
        dataSet=open(self.cleanData, 'r')
        for line in dataSet:
            line.replace('\n', '')
            columns = line.split('\t')
            user = columns[0]
            movie = columns[1]
            rating = columns[2]
            if user not in userSet:
                userSet.add(user)
                moviesRatedByUserDict[user]={}
            moviesRatedByUserDict[user][movie]= rating
        dataSet.close()
        return moviesRatedByUserDict

    def movieTagAsKeyDict(self):
        # returns a dict with tags as keys and all movies that share tag as values
        movieSet = set()
        data=open(self.cleanData, 'r')
        for line in data:
            columns = line.split('\t')
            movie = columns[1]
            if movie not in movieSet:
                movieSet.add(movie)
        data.close()
        
        tagSet = set()
        movieTags = open(self.movieTag, 'r')
        movieTagAsKeyDict = {}
        for line in movieTags:
            if line != '\n':
                line = line.replace('\n', '')
                columns = line.split('\t')
                movie = columns[0]
                if movie in movieSet: # we only care about movie tags for movies in our data set
                    allTags = columns[1]
                    tagList = allTags.split(',')
                    for tag in tagList:
                        if tag not in tagSet:
                            tagSet.add(tag)
                            movieTagAsKeyDict[tag]=[]
                        movieTagAsKeyDict[tag].append(movie)
        return movieTagAsKeyDict

    def meanMovieRatingDict(self):
        # returns dictionary with average rating for each movie, max rating
        maxRating = 0
        data = open(self.meanMovieRating,'r')
        meanMovieRatingDict = {}
        for line in data:
            line = line.replace('\n', '')
            columns = line.split('\t')
            movie = columns[0]
            rating = columns[1]
            meanMovieRatingDict[movie]=rating
            if float(rating) > maxRating:
                maxRating = float(rating)
        return meanMovieRatingDict, maxRating

    def userHistoryDict(self):
        # returns a dict with user as keys and list of history tags (movies) as values
        historyData = open(self.historyTag, 'r')
        userSet=set()
        historyDict = {}
        for line in historyData:
            if line != '\n':
                line = line.replace('\n', '')
                columns = line.split('\t')
                user = columns[0]
                movieString = columns[1]
                movieList = movieString.split(',')
                if user not in userSet:
                    userSet.add(user)
                    historyDict[user]=[]
                for movie in movieList:
                    historyDict[user].append(movie)
        historyData.close()
        return historyDict

    def userSocialDictReader(self):
        # returns a dict with user as keys and list of friends as values
        data = open(self.social, 'r')
        socialDict = {}
        for line in data:
            if line != '\n':
                line = line.replace('\n', '')
                columns = line.split('\t')
                user = columns[0]
                friendString = columns[1]
                friendList = friendString.split(',')
                socialDict[user]=[]
                for friend in friendList:
                    socialDict[user].append(friend)
        data.close()
        return socialDict
    
###############################
############# Run #############

    def run(self,sproc,subprocesses):

        cvStr = self.libFMBinary + ' -task r -train ' + \
            self.runTrain + ' -test ' + \
            self.runCV + ' -init_stdev ' + \
            self.initStd + ' -dim \'' + \
            self.globalBias + ','+ \
            self.oneWay + ','+ \
            self.dims + '\' -iter ' + \
            self.strItr + ' -rlog '+  \
            self.logCV + ' -out ' + \
            self.predCVTmp
        cvArr = cvStr.split()
        testStr = self.libFMBinary + ' -task r -train ' + \
            self.runTrain + ' -test ' + \
            self.runTest + ' -init_stdev ' + \
            self.initStd + ' -dim \'' + \
            self.globalBias + ','+ \
            self.oneWay + ','+ \
            self.dims + '\' -iter ' + \
            self.strItr + ' -rlog '+  \
            self.logTest + ' -out ' + \
            self.predTestTmp
        testArr = testStr.split()
        ### CV ###
        pCV = sproc.Popen(cvArr,shell=False)
        pTest = sproc.Popen(testArr,shell=False)
        subprocesses.append(pTest)
        subprocesses.append(pCV)
