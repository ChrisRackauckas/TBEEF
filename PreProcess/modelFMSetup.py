def FMSetup(os, utils):
	osStr = 'perl Models/libFM/triple_format_to_libfm.pl -in ' + utils.PROCESSED_TRAIN_PATH + ',' + utils.TEST_IDS_DUMMY_PATH + ',' + utils.PROCESSED_CV_PATH + ' -target 2 -separator \"\\t\"'
	os.system(osStr)
	os.system('./Models/libFM/convert --ifile ' + utils.PROCESSED_TRAIN_PATH + '.libfm ' + '--ofilex ' + utils.FM_TRAIN_BIN_PATH + '.x --ofiley ' + utils.FM_TRAIN_PATH + '.y') 
	os.system('./Models/libFM/convert --ifile ' + utils.PROCESSED_CV_PATH + '.libfm ' + '--ofilex ' + utils.FM_CV_BIN_PATH + '.x --ofiley ' + utils.FM_CV_PATH + '.y')
	os.system('./Models/libFM/convert --ifile ' + utils.TEST_IDS_DUMMY_PATH + '.libfm ' + '--ofilex ' + utils.FM_TEST_BIN_PATH + '.x --ofiley ' + utils.FM_TEST_PATH + '.y')
	os.system('./Models/libFM/transpose --ifile ' + utils.FM_TRAIN_BIN_PATH + '.x --ofile ' + utils.FM_TRAIN_PATH + '.xt')
	os.system('./Models/libFM/transpose --ifile ' + utils.FM_TEST_BIN_PATH + '.x --ofile ' + utils.FM_TEST_PATH + '.xt')
	os.system('./Models/libFM/transpose --ifile ' + utils.FM_CV_BIN_PATH + '.x --ofile ' + utils.FM_CV_PATH + '.xt')	
