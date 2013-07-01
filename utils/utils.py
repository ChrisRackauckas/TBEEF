#### Paths ####

template = 'bin/libFM -task r -train training_set_nodups.libfm -test predict_dummy.libfm -dim ’1,1,8’ -out colin_test8.txt'
TEST_IDS_PATH = 'Data/Original/predict.txt'
TEST_IDS_DUMMY_PATH = 'Data/Original/predict_dummy.txt'
ORIGINAL_TRAIN_PATH = 'Data/Original/training_set_nodups_random.txt'

#### FM ####

FM_TRAIN_PATH = 'Data/ModelData/FMTrain.txt'
FM_TEST_PATH = 'Data/ModelData/FMTest.txt'
FM_ITER = 50
FM_STR_ITER = str(FM_ITER)
FM_GLOBAL_BIAS = '1' #either 1 or 0
FM_ONE_WAY_INTERACTION = '1' #either 1 or 0
FM_PREDICTIONS_PATH = 'Data/Output/iter_'+FM_STR_ITER
FM_DIMS = [ '1', '2']