def postProcess(os,utils, DE_EFFECT):

#-----------------------------------------------------------------
# Reads in prediction data file with (userID, movieID, effected rating)
#       rating and Re-effects data (to 1 to 5 range)
#-----------------------------------------------------------------

        utils.fixTestPredictions(utils.TEST_IDS_PATH,utils.HYBRID_SYNTHESIZED_PATH, \
                utils.TO_POST_PATH)
	#findPairs(os,utils,utils.ORIGINAL_DATA_PATH,utils.TO_POST_PATH,utils.OUTPUT_PATH)

        if DE_EFFECT:
                globalMeanFile = open(utils.EFFECTS_GLOBAL_PATH, 'r')
                globalMean = float(globalMeanFile.read())
                globalMeanFile.close()
            
                infile = open(utils.TO_POST_PATH, 'r')
                outfile = open(utils.OUTPUT_PATH, 'w')
                for line in infile:
                        line = line.replace('\n', '')
                        columns = line.split('\t')
                        user = columns[0]
                        movie = columns[1]
                        newRating = globalMean + float(columns[2])
                        outfile.write(user+'\t'+movie+'\t'+ str(newRating)+'\n')
                infile.close()
                outfile.close()

        else:
                os.system('cp '+ utils.TO_POST_PATH +' '+ utils.OUTPUT_PATH)

def findPairs(os,utils,masterPath,changePath,toSave):
	masterFile = open(masterPath, 'r')
	changeFile = open(changePath, 'r')
	masterLines = masterFile.readlines()
	changeLines = changeFile.readlines()
	maxX = len(masterLines)	

	toWrite = []
	for master in masterLines:
		for change in changeLines:
			toWrite.append(change[:-7])
			if master[:-7]==change[:-7]:
				toWrite.append(master[17:])
			else:
				toWrite.append(change[17:])
	toWrite[len(toWrite)] = toWrite[len(toWrite)][:-2]
	outfile = open(toSave, 'w')
    	outfile.writelines(["%s" % item  for item in toWrite])
