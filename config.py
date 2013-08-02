################### Select Models ##################

models = [
          #['basicFM','FM','Basic',['2']],
          #['bmt','FM','BasicMovieTag',['2']],
          #['amt','FM','AdjustedMovieTag',['2']]
          #['nn', 'FM', 'NearestNeighbor',['2']]
          #['rmt','FM','RelatedMovieTag',['2']]
    
          #['basicSVD','SVD','Basic',[]]
          ['ImplicitFeedbackSVD','SVD','ImplicitFeedback',[]]
          #['NeighborhoodMovieTag', 'SVD' , 'Neighborhood' , ['MovieTag']]
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
                 #['RFR' ,'RFR' ,[]],  # Large memory requirement
                  ['Lasso', 'Lasso', []]
                 #['GBRT','GBRT',['10']]
]

# Defining ensemble models:
# Each element is a list:
# [tag,modelType,misc]
# tag is the name of the model
# modelType defines what model to use
# misc is the arguments to the program

synthModel = ['GBRT','GBRT',['10']]

################### Select Parts  ##################
LAPTOP_TEST      = True # uses small data set to run features on laptop

TRIALS           = 1 
PRE_PROCESS      = True
# ---- ---- PreProcess Selection ---- ---- #
TEST_SUBSET      = True   # uses small data set

### Baidu Specific Preprocess ###
PROCESS_TAGS     = False  # generates new file for movie tag feature
PROCESS_SOCIAL   = True  # cuts out all the extra social users not in data set
PROCESS_HISTORY  = True
### End Baidu Specific ####

DE_EFFECT        = False  # If De-effect is false, intermittent predictions are correct
# ---- ---- ---- ---- ----- ---- ---- ---- #
SETUP_MODELS     = True
RUN_MODELS       = True
SETUP_HYBRID     = False
RUN_HYBRID       = False
SETUP_SYNTHESIZE = False
RUN_SYNTHESIZE   = False
POST_PROCESS     = False


################## Select Bootstrap Parameters  ##################

BOOTSTRAP_SPLITS = [.8, .8, .8]

################## Timer  ##############

TIME_RUN     = False

################## Factorization Machines ##########

FM_ITER = 40
FM_STR_ITER = str(FM_ITER)
FM_INIT_STD = '.3'

################## SVD Feature #####################

SVD_LEARNING_RATE         = '.005'
SVD_REGULARIZATION_ITEM   = '.004'
SVD_REGULARIZATION_USER   = '.004'
SVD_REGULARIZATION_GLOBAL = '.001'
SVD_REGULARIZATION_FEEDBACK = '.004'
SVD_NUM_FACTOR            = '64'
SVD_ACTIVE_TYPE           = '0'
SVD_NUM_ITER              = '40'

################## Hybrid #########################

