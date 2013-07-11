def postProcess(os,utils, DE_EFFECT,trials):
#-----------------------------------------------------------------
# Reads in prediction data file with (userID, movieID, effected rating)
#       rating and Re-effects data (to 1 to 5 range)
#-----------------------------------------------------------------

    for trial in range(0,trials):
        strTrial = str(trial)
        umr = utils.userMovieRating
        predTest    = utils.SYNTH_PREDICT_PATH + self.tag\
                          + '_test_t' + strTrial
        trialOutput = utils.TRIAL_OUTPUT_PATH + 't' + strTrial 
        if DE_EFFECT:
            reEffect(predTest,trialOutput)
        else:
            os.system('cp '+ predTest +' '+ trialOutput)

    winner = pickWinner(trials)

    os.system('cp ' + trialOutput + ' ' + utils.OUTPUT_PATH)

def reEffect(inputFile,outputFile):
    globalMeanFile = open(utils.EFFECTS_GLOBAL_PATH, 'r')
    globalMean = float(globalMeanFile.read())
    globalMeanFile.close()
    infile = open(inputFile, 'r')
    outfile = open(outputFile, 'w')
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

def pickWinner(trials): 
    trialsOut = '0'
