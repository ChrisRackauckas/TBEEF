#### Paths ####

TEST_IDS_PATH = 'Data/Original/predict.txt'
TEST_IDS_DUMMY_PATH = 'Data/PreProcessed/predict_dummy.txt'
ORIGINAL_DATA_PATH = 'Data/Original/data_set.txt'
ORIGINAL_DATA_RNDM_NODUPS_PATH = 'Data/Original/data_set_rndm_nodups.txt'
PROCESSED_DATA_PATH = 'Data/PreProcessed/data_set_processed.txt'
PROCESSED_TRAIN_PATH = 'Data/PreProcessed/training_set_processed.txt'
PROCESSED_CROSSVAL_PATH = 'Data/PreProcessed/crossVal_set_processed.txt'

EFFECTS_USER_PATH = 'Data/Effects/user_effects.txt'
EFFECTS_MOVIE_PATH = 'Data/Effects/movie_effects.txt'
EFFECTS_GLOBAL_PATH = 'Data/Effects/global_effects.txt'

#### DATA ####

DATA_SET_SPLIT = .8 # percent of data for training, 1-value is for cross validation


#### FM ####

FM_TRAIN_PATH = 'Data/ModelData/FMTrain.txt'
FM_TEST_PATH = 'Data/ModelData/FMTest.txt'
FM_ITER = 50
FM_STR_ITER = str(FM_ITER)
FM_GLOBAL_BIAS = '1' #either 1 or 0
FM_ONE_WAY_INTERACTION = '1' #either 1 or 0
FM_PREDICTIONS_PATH = 'Data/ModelPredictions/FMPredictionIter_'+FM_STR_ITER
FM_DIMS = [ '1', '2']
