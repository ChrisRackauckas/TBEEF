def postProcess(os,utils, DE_EFFECT):

#-----------------------------------------------------------------
# Reads in prediction data file with (userID, movieID, effected rating)
#       rating and Re-effects data (to 1 to 5 range)
#-----------------------------------------------------------------

        utils.fixTestPredictions(utils.TEST_IDS_PATH,utils.HYBRID_SYNTHESIZED_PATH, \
                utils.TO_POST_PATH)

        umr = utils.userMovieRating
        
        if DE_EFFECT:
                globalMeanFile = open(utils.EFFECTS_GLOBAL_PATH, 'r')
                globalMean = float(globalMeanFile.read())
                globalMeanFile.close()
            
                infile = open(utils.TO_POST_PATH, 'r')
                outfile = open(utils.RE_EFFECT_PATH, 'w')
                for line in infile:
                        line = line.replace('\n', '')
                        columns = line.split('\t')
                        user = columns[0]
                        movie = columns[1]
                        newRating = globalMean + float(columns[2])
                        if newRating > 5.0:
                                newRating = 5.0

                        #check to see if user,movie pair is in original data
                        if user in umr:
                                umrUserMovies = umr[user][0]
                                umrUserRatings = umr[user][1]
                                for i in range(len(umrUserMovies)):
                                        if umrUserMovies[i] == movie:
                                                newRating = umrUserRatings[i]
                                        
                        outfile.write(user+'\t'+movie+'\t'+ str(newRating)+'\n')
                infile.close()
                outfile.close()

        else:
                os.system('cp '+ utils.TO_POST_PATH +' '+ utils.RE_EFFECT_PATH)


