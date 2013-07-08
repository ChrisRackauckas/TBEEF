################### Select Models ##################

models = [['basicFM','FM','Basic',['2']]] 

# Defining models:
# Each element is a list: 
# [tag,program,setting,misc]
# tag is the name of the model
# program specifies which program to use
# setting defines which features will be used
# Misc depends on the program:
# For FM: [dims]
# For SVDFeature: []

ensembleModels = [['OLSR','OLS',[]]]

# Defining ensamble models:
# Each element is a list:
# [tag,modelType,misc]
# tag is the name of the model
# modelType defines what model to use
# misc is the arguments to the program

################### Select Parts  ##################

PRE_PROCESS      = True
DE_EFFECT        = True
SETUP_MODELS     = True
RUN_MODELS       = True
SETUP_HYBRID     = True
RUN_HYBRID       = False
POST_PROCESS     = False
HYBRID_CHOICE    = 1

################## Select Bootstrap Size  ##################

BOOTSTRAP_SIZE_TRAIN = 50000
BOOTSTRAP_SIZE_CV    = 10000

################## Select Performance ##############

RUN_PARALLEL = True
TIME_RUN     = False

################## Factorization Machines ##########

FM_ITER = 100
FM_STR_ITER = str(FM_ITER)
FM_INIT_STD = '.3'

################## Hybrid #########################

