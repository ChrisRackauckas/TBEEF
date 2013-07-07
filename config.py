################### Select Parts  ##################

PRE_PROCESS  = True
DE_EFFECT    = False
RANDOMIZE_DATA = True
SETUP_FM     = True
RUN_FM       = False
SETUP_HYBRID = False
RUN_HYBRID   = False
POST_PROCESS = False
HYBRID_CHOICE = 1

################### Select Features  ##################
FEATURES = True

MOVIE_TAG = True
SOCIAL = False
HISTORY = False

################## Select Performance ##############

RUN_PARALLEL = True
RUN_SERIAL   = False
TIME_RUN     = False


################## Factorization Machines ##########

FM_ITER = 100
FM_DIMS = [ '1', '2']
FM_STR_ITER = str(FM_ITER)
FM_INIT_STD = .3

################## Hybrid #########################

RR_CONST = 1

