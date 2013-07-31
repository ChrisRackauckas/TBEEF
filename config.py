################### Select Models ##################

models = [
    ['basicFM', 'FM', 'Basic', ['8']],
    #['bmt','FM','BasicMovieTag',['2']],
    ['amt','FM','AdjustedMovieTag',['2']],
    #['nn', 'FM', 'NearestNeighbor',['2']],
    #['rmt','FM','RelatedMovieTag',['2']],

    ['basicSVD', 'SVD', 'Basic', []]
]

# Defining models:
# Each element is a list: 
# [tag,program,setting,misc]
# tag is the name of the model
# program specifies which program to use
# setting defines which features will be used
# Misc depends on the program:
# For FM: [dims]
# For SVDFeature: []

ensembleModels = [['OLSR', 'OLS', []],
                  ['OLSI','OLSI',['2']],
                  ['RR'  ,'RR',['2']],
                  ['BRT','BRT',[]],
                  ['BMAR','BMAR',[]],
                 #['RFR' ,'RFR' ,[]],
                  ['Lasso', 'Lasso', []],
                  ['GBRT','GBRT',['10']]
]

# Defining ensemble models:
# Each element is a list:
# [tag,modelType,misc]
# tag is the name of the model
# modelType defines what model to use
# misc is the arguments to the program

synthModel = ['GBRT','GBRT',['10']]

################### Select Parts  ##################
TEST_SUBSET = True          # uses small data set

TRIALS = 2
PRE_PROCESS = True
PROCESS_TAGS = True
PROCESS_SOCIAL = True
PROCESS_HISTORY = True
DE_EFFECT = False           # If De-effect is false, model predictions are correct
SETUP_MODELS = True
RUN_MODELS = True
SETUP_HYBRID = True
RUN_HYBRID = True
SETUP_SYNTHESIZE = True
RUN_SYNTHESIZE = True
POST_PROCESS = True

################## Select Bootstrap Parameters  ##################

BOOTSTRAP_SPLITS = [.8, .8, .8]

################## Timer  ##############

TIME_RUN = False

################## Factorization Machines ##########

FM_ITER = 40
FM_STR_ITER = str(FM_ITER)
FM_INIT_STD = '.3'

################## SVD Feature #####################

SVD_LEARNING_RATE = '.005'
SVD_REGULARIZATION_ITEM = '.004'
SVD_REGULARIZATION_USER = '.004'
SVD_REGULARIZATION_GLOBAL = '.001'
SVD_NUM_FACTOR = '64'
SVD_ACTIVE_TYPE = '0'
SVD_NUM_ITER = '40'

################## Hybrid #########################

