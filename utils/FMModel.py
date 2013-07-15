from Model import Model
class FMModel(Model):
   
### Constructors ########
    
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
        self.historyTag             = utils.USER_HISTORY_PATH
        self.social                 = utils.USER_SOCIAL_PATH
        
### Setup Data ###

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
        
        os.sys.stdout.write('{0}\r'.format('-- Converting (1/6) --') )
        os.system('./Models/libFM/convert --ifile ' + 
            self.featTrain + 
            '.libfm ' + '--ofilex ' + 
            self.tmpTrain + 
            '.x --ofiley ' + 
            self.runTrain + '.y' +
            '> /dev/null')
        os.sys.stdout.write('{0}\r'.format('-- Converting (2/6) --') )
        os.system('./Models/libFM/convert --ifile ' + 
            self.featCV + 
            '.libfm ' + '--ofilex ' + 
            self.tmpCV +
            '.x --ofiley ' + 
            self.runCV + '.y' +
            '> /dev/null')
        os.sys.stdout.write('{0}\r'.format('-- Converting (3/6) --') )
        os.system('./Models/libFM/convert --ifile ' + 
            self.featTest + 
            '.libfm ' + '--ofilex ' + 
            self.tmpTest + 
            '.x --ofiley ' + 
            self.runTest + '.y'
            '> /dev/null')
        os.sys.stdout.write('{0}\r'.format('-- Converting (4/6) --') )
        os.system('./Models/libFM/transpose --ifile ' + 
            self.tmpTrain + 
            '.x --ofile ' + 
            self.runTrain + '.xt' +
            '> /dev/null')
        os.sys.stdout.write('{0}\r'.format('-- Converting (5/6) --') )
        os.system('./Models/libFM/transpose --ifile ' + 
            self.tmpTest + 
            '.x --ofile ' + 
            self.runTest + '.xt' +
            '> /dev/null')
        os.sys.stdout.write('{0}\r'.format('-- Converting (6/6) --') )
        os.system('./Models/libFM/transpose --ifile ' + 
            self.tmpCV + '.x --ofile ' + 
            self.runCV + '.xt' + 
            '> /dev/null')
        print()

### Develop Features ###

    def setupFeatures(self):
        import os
        #-----------------------------------------------------------------
        # creates the features for LibFM, then turns into sparse matrix
        #----------------------------------------------------------------- 
        if self.featureSet == 'Basic':
            os.system('cp ' + self.bootTrain + ' ' + self.featTrain)
            os.system('cp ' + self.bootCV    + ' ' + self.featCV   )
            os.system('cp ' + self.bootTest  + ' ' + self.featTest )
            self.libFMFormat(2)

        if self.featureSet == 'BasicMovieTag':
            print('...Adding Basic Movie Tag Data')
            self.basicMovieTag(self.bootTrain,self.featTrain)
            self.basicMovieTag(self.bootCV,self.featCV)
            self.basicMovieTag(self.bootTest,self.featTest)
            self.libFMFormat(2)

        if self.featureSet == 'AdjustedMovieTag':
            print('...Adding Adjusted Movie Tag Data')
            self.adjustedMovieTag(self.bootTrain,self.featTrain)
            self.adjustedMovieTag(self.bootCV,self.featCV)
            self.adjustedMovieTag(self.bootTest,self.featTest)

        if self.featureSet == 'NearestNeighbor':
            print('...Adding Nearest Neighbor Data')
            self.addNearestNeighbor(self.bootTrain,self.featTrain)
            self.addNearestNeighbor(self.bootCV,self.featCV)
            self.addNearestNeighbor(self.bootTest,self.featTest)

        if self.featureSet == 'RelatedMovieTag':
            print('...Adding Related Movie Tag Data')
            self.relatedMovieTag(self.bootTrain,self.featTrain)
            self.relatedMovieTag(self.bootCV,self.featCV)
            self.relatedMovieTag(self.bootTest,self.featTest)


    def basicMovieTag(self,finPath, foutPath):
        import os
        #-----------------------------------------------------------------
        # creates new data set with movie tag info by appending tags as columns
        # Output data still needs to by formatted for LibFM
        #-----------------------------------------------------------------

        lineCount= self.lineCount(finPath)
        counter=0
        
        tagDict = self.movieTagDict()
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

                if counter%100==0:
                    # prints read-out that shows how quickly data is being written
                    os.sys.stdout.write('{0}\r'.format( \
                        str('-- '+str('{0:.2f}'.format(counter/lineCount*100))+ \
                        ' percent of data formatted --'))
                        )
                counter +=1
        os.sys.stdout.write('{0}\r'.format( \
            '-- Formatting Complete --            ')) # space included on purpose to overwrite previous string
        print()
        dataSet.close()
        dataSetWithTags.close()

    def adjustedMovieTag(self,finPath, foutPath):
        import os
        #-----------------------------------------------------------------
        # creates sparse matrix with movie tags where output for tags is
        # column:1/m where m is the total num tags for the movie
        #-----------------------------------------------------------------

        lineCount= self.lineCount(finPath)
        counter=0
        
        userLocationDict, movieLocationDict = self.userMovieLocationDict()
        startVal = len(userLocationDict)+len(movieLocationDict)
        tagDict, tagLocationDict = self.movieTagAndLocationDict(startVal)
        dataSet = open(finPath,'r')
        fout = open(foutPath,'w')
        for line in dataSet:
            if line != '\n':
                line = line.replace('\n', '')
                columns = line.split('\t')
                user=columns[0]
                movie = columns[1]
                rating= columns[2]
                movCol = movieLocationDict[movie]
                userCol = userLocationDict[user]
                if movie in tagDict:
                    string=''
                    m = len(tagDict[movie])
                    val = str( '{0:.4f}'.format( 1/m ) ) # 1/m
                    for tag in tagDict[movie]:
                        string=string+tagLocationDict[tag]+':'+val+' '
                    string=string[:-1]
                    fout.write(rating+' '+userCol+':1 '+movCol+':1 '+string+'\n')
                else:
                    fout.write(rating+' '+userCol+':1 '+movCol+':1\n')

                if counter%100==0:
                    # prints read-out that shows how quickly data is being written
                    os.sys.stdout.write('{0}\r'.format( \
                        str('-- '+str('{0:.2f}'.format(counter/lineCount*100))+ \
                        ' percent of data formatted --'))
                        )
                counter +=1
        os.sys.stdout.write('{0}\r'.format( \
            '-- Formatting Complete --            ')) # space included on purpose to overwrite previous string
        print()
        dataSet.close()
        fout.close()
        os.system('mv '+foutPath+' '+foutPath+'.libfm')

    def addNearestNeighbor(self,finPath, foutPath):
        import os
        #-----------------------------------------------------------------
        # creates sparse matrix where non-user/movie entries given as column:rating/m
        # where m is the total number of movies rated by the user
        #-----------------------------------------------------------------

        moviesRatedByUser = self.movisRatedByUserDict()
        movieLocationDict = self.movieLocationDict()
        lineCount= self.lineCount(finPath)

        totalMovies = len(movieLocationDict)
        fin = open(finPath, 'r')
        fout = open(foutPath, 'w')
        counter = 0
        for line in fin:
            line.replace('\n', '')
            columns = line.split('\t')
            user = columns[0]
            movie = columns[1]
            rating = columns[2]
            movCol = movieLocationDict[movie]
            string=''   
            m = len(moviesRatedByUser[user])    # num of movies rated by user
            for thing in moviesRatedByUser[user]:
                mov = thing[0]    # other rated movie by same user
                rate = thing[1]    # other movie's rating
                location = str( int(movieLocationDict[mov])+totalMovies )
                val = str( '{0:.4f}'.format( float(rate)/m ) ) # r/m
                string = string + location+':'+val+' '
            string=string[:-1]  # gets rid of the extra space on the end
            fout.write(rating[:-1]+' '+movCol+':1 '+string+'\n')

            if counter%50==0:
                # prints read-out that shows how quickly data is being written
                os.sys.stdout.write('{0}\r'.format( \
                    str('-- '+str('{0:.2f}'.format(counter/lineCount*100))+ \
                        ' percent of data formatted --'))
                        )
            counter +=1
        os.sys.stdout.write('{0}\r'.format( \
            '-- Formatting Complete --            ')) # space included on purpose to overwrite previous string
        print()
        fin.close()
        fout.close()
        
        os.system('mv '+foutPath+' '+foutPath+'.libfm')

    def relatedMovieTag(self,finPath, foutPath):
        import os
        #-----------------------------------------------------------------
        # creates sparse matrix using movie tags with movie id, then columns
        #  where movies that share tags are given a 1/m value, m is total
        #  movies with a given tag
        #-----------------------------------------------------------------

        lineCount= self.lineCount(finPath)
        counter=0
        
        userLocationDict, movieLocationDict = self.userMovieLocationDict()
        movieTagDict = self.movieTagDict()
        relatedMovieDict = self.relatedMovieDict()
        offset = len(movieLocationDict)
        
        dataSet = open(finPath,'r')
        fout = open(foutPath,'w')
        for line in dataSet:
            if line != '\n':
                line = line.replace('\n', '')
                columns = line.split('\t')
                user=columns[0]
                movie = columns[1]
                rating= columns[2]
                movCol = movieLocationDict[movie]
                userCol = userLocationDict[user]
                if movie in movieTagDict:
                    string=''
                    m = 0   # num related movies
                    for tag in movieTagDict[movie]:
                        m += len(relatedMovieDict[tag])
                    val = str( '{0:.4f}'.format( 1/m ) ) # 1/m
                    for tag in movieTagDict[movie]:
                        for relatedMovie in relatedMovieDict[tag]:
                            loc = int(movieLocationDict[relatedMovie])+offset
                            string=string+str(loc)+':'+val+' '
                    string=string[:-1]
                    fout.write(rating+' '+userCol+':1 '+movCol+':1 '+string+'\n')
                else:
                    fout.write(rating+' '+userCol+':1 '+movCol+':1\n')

                if counter%100==0:
                    # prints read-out that shows how quickly data is being written
                    os.sys.stdout.write('{0}\r'.format( \
                        str('-- '+str('{0:.2f}'.format(counter/lineCount*100))+ \
                        ' percent of data formatted --'))
                        )
                counter +=1
        os.sys.stdout.write('{0}\r'.format( \
            '-- Formatting Complete --            ')) # space included on purpose to overwrite previous string
        print()
        dataSet.close()
        fout.close()
        os.system('mv '+foutPath+' '+foutPath+'.libfm')

### Helpful Functions for adding Features ###

    def lineCount(self,finPath):
        # returns a line count on the input file
        fin = open(finPath, 'r')    
        lineCount=0
        for line in fin:
            lineCount+=1
        fin.close()
        return lineCount


    def movieLocationDict(self):
        # returns a dict with movies as keys and location in sparse matrix as value
        movieSet=set()
        movieLocation = 1
        movieLocationDict={}   
        
        dataSet=open(self.cleanData, 'r')
        for line in dataSet:
            columns = line.split('\t')
            movie = columns[1]
            if movie not in movieSet:
                movieSet.add(movie)
                movieLocationDict[movie] = str(movieLocation)
                movieLocation +=1
        dataSet.close()
        return movieLocationDict

    def userMovieLocationDict(self):
        # returns two dicts, one with movies as keys and
        #  and the other with users as keys. Both hold location in sparse matrix as value
        movieSet=set()
        userSet=set()
        location = 1
        movieLocationDict={}
        userLocationDict={}
        # first time through we get user locations
        dataSet=open(self.cleanData, 'r')
        for line in dataSet:
            columns = line.split('\t')
            user = columns[0]
            if user not in userSet:
                userSet.add(user)
                userLocationDict[user]= str(location)
                location += 1
        dataSet.close()
        # this time get movie locations
        dataSet=open(self.cleanData, 'r')
        for line in dataSet:
            columns = line.split('\t')
            movie = columns[1]
            if movie not in movieSet:
                movieSet.add(movie)
                movieLocationDict[movie] = str(location)
                location +=1
        dataSet.close()
        return userLocationDict,movieLocationDict


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
        # returns a dict with user as keys and a list of all (movie,rating) tuples for the given user
        userSet=set()
        movieSet=set()   
        moviesRatedByUser = {}
        
        dataSet=open(self.cleanData, 'r')
        for line in dataSet:
            line.replace('\n', '')
            columns = line.split('\t')
            user = columns[0]
            movie = columns[1]
            rating = columns[2]
            if user not in userSet:
                userSet.add(user)
                moviesRatedByUser[user]=[]
            moviesRatedByUser[user].append( (movie, rating) )
        dataSet.close()
        return moviesRatedByUser

    def relatedMovieDict(self):
        # returns a dict with tags as keys and all movies that share tag as values
        tagSet = set()
        movieTags = open(self.movieTag, 'r')
        relatedMovieDict = {}
        for line in movieTags:
            if line != '\n':
                line = line.replace('\n', '')
                columns = line.split('\t')
                movie = columns[0]
                allTags = columns[1]
                tagList = allTags.split(',')
                for tag in tagList:
                    if tag not in tagSet:
                        tagSet.add(tag)
                        relatedMovieDict[tag]=[]
                    relatedMovieDict[tag].append(movie)
        return relatedMovieDict
    

### Run ###

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
