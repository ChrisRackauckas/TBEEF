def postProcess(os,utils):
	utils.fixTestPredictions(utils.TEST_IDS_PATH,utils.HYBRID_SYNTHESIZED_PATH,utils.TO_POST_PATH)
	#findPairs(os,utils,utils.ORIGINAL_DATA_PATH,utils.TO_POST_PATH,utils.OUTPUT_PATH)

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
