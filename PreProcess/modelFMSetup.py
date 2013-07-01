def FMSetup(os, utils):
	osStr = 'perl Models/libFM/triple_format_to_libfm.pl -in ' + utils.ORIGINAL_TRAIN_PATH + ',' + utils.TEST_IDS_DUMMY_PATH + ' -target 2 -separator \"\\t\"'
	os.system(osStr)
	os.system('mv ' + utils.ORIGINAL_TRAIN_PATH + '.libfm ' + utils.FM_TRAIN_PATH)
	os.system('mv ' + utils.TEST_IDS_DUMMY_PATH + '.libfm ' + utils.FM_TEST_PATH) 
