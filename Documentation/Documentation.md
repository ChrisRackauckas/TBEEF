Hybrid Movie Recommendation System Documentation
==============================================

This program is a hybrid recommendation system. This documentation is written for those who wish to modify the program in some manner or join the effect. 

Program Structure
----------------------------------------------

Data Structures
----------------------------------------------------

The main data structures of the program are as follows:

1. Models. For computational efficiency purposes (and the fact that they are reasonably simple and rarely written to), models are defined using arrays instead of objects. Models start by definition by the user in the configuration file, config.py. The user specifies the models as follows:
    
    [tag,program,featureSet,[misc]]

- Tag is a unique identifier to the model. It must be unique in order to ensure the models do no overwrite eachother's data files.
- Program is a string, either 'FM' or 'SVD', which states whether the model should be evaluated using either libFM or SVDFeature respectively.
- Feature set is a parameter that lets the user choose which feature set the models should use. To know which features are implemented, look inside the PreProcess directory to find the libFM and SVDFeature setup directories. Inside each of these directories should be a file titled -FeatureSetup.py. These are the folders where the feature choice process occurs. Look for conditional statements based on model[2], these are the statements that check the feature set parameter.
- Misc is a list of miscellaneous parameters for controlling the models. Currently, the choices are as follows:

--libFM: ['dimensions']
--SVD: []

At the model setup phase, these are converted into a larger model for the purpose of calculation. These are then saved into modelData, an array stored in utils/utils.py. This stucture is defined as follows:

    [tag,program,featureSet,[misc],[paths],trial]

The first four options are copied from the array before. The last two are defined as follows:

- Paths is a list of relevant paths for model setup. The list is in the following order:

--bootTrain : Training dataset given by bootsplit
--bootCV : CV dataset given by bootsplit
--bootTest : Test dataset with dummy variables (required for computation)
--featTrain 
--featCV
--featTest
--tmpTrain
--tmpCV
--tmpTest
--runTrain : Training dataset for the model to run
--runCV : CV dataset for the model to run
--runTest : Test dataset for the model to run
--predCV : Where the predictions from the CV dataset are saved
--predTest : Where the predictions from the Test dataset are saved
--logCV : Where the logfile for the CV run is saved (libFM)
--logTest : Where the logfile for the Test run is saved (libFM)
--configPath : Where the config file for the run is saved (SVDFeature)

As for the feat and tmp datasets, their order is defined by the program choice. The flow is as follows for libFM. 
