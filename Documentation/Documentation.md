Hybrid Movie Recommendation System Documentation
==============================================

This program is a hybrid recommendation system. This documentation is written for those who wish to modify the program in some manner or join the effect. 

Program Structure
----------------------------------------------

The program runs as follows. The driver is the brains of the program, directing the entire scheme. It first calls a pre-processing step which takes the data from Original and saves out pre-processed forms to PreProcessed. Then the model setup phase begins. First, the model objects are constructed. Then, they call their setup methods which generates datafiles in ModelSetup until they produce the files for runtime which are saved in ModelData. Then the model's run methods are called. They read in the data from ModelData and saves out predictions to ModelPredictions. These predictions are then aggregated into the HybridSetup folder. The ensemble methods are then called and they take the data from HybridSetup to produce the files in HybridPredictions. Then this prediction matrix is ran through a gradient boosted regression to produce the files in FinalCross. The post processor looks at the datasets in FinalCross and takes the one with the lowest RMSE on a CV set to be the best predicting model, and so it takes the associated test dataset predictions from there and post-processes them to save in output.

Data Structures
----------------------------------------------------

The main data structures of the program are as follows:

1. Models are defined as an object. Models start by definition by the user in the configuration file, config.py. The user specifies the models as follows:
    
    [tag,program,featureSet,[misc]]

- Tag is a unique identifier to the model. It must be unique in order to ensure the models do no overwrite eachother's data files.
- Program is a string, either 'FM' or 'SVD', which states whether the model should be evaluated using either libFM or SVDFeature respectively.
- Feature set is a parameter that lets the user choose which feature set the models should use. To know which features are implemented, look inside the PreProcess directory to find the libFM and SVDFeature setup directories. Inside each of these directories should be a file titled -FeatureSetup.py. These are the folders where the feature choice process occurs. Look for conditional statements based on model[2], these are the statements that check the feature set parameter.
- Misc is a list of miscellaneous parameters for controlling the models. Currently, the choices are as follows:

--libFM: ['dimensions']
--SVD: []

At the model setup phase, these are converted into an object defined in utils for the purpose of calculation. These are then saved into modelList, an array stored in driver. The methods and fields are defined as follows:

-tag : a unique identifier for the model
-mode : defines which program to use, choices are 'FM' and 'SVD'
- featureSet : defines which feature set to use. See the model's setupFeatures method for options
- misc : the array passed in as misc
- trial : the trial the model is assigned to
- Setup Data Paths:
--bootTrain : Training dataset given by bootsplit
--bootCV : CV dataset given by bootsplit
--bootTest : Test dataset with dummy variables (required for computation)
--featTrain : The training dataset just after features are added
--featCV : The CV dataset just after features are added
--featTest : The Test dataset just after features are added
--tmpTrain : Temporary dataset in the setup process
--tmpCV : Temporary dataset in the setup process
--tmpTest : Temporary dataset in the setup process
--runTrain : Training dataset for the model to run
--runCV : CV dataset for the model to run
--runTest : Test dataset for the model to run
--predCV : Where the predictions from the CV dataset are saved
--predTest : Where the predictions from the Test dataset are saved

-Feature Paths: These are used for feature creation
- movieTagPath : Path to the movie tag dataset
- userSocialPath : Path to the user social dataset
- userHistoryPath : Path to the user history dataset

The Model is class is not used directly. Rather, it is used through two subclasses, FMModel and SVDModel, which are determined by the mode. These have extra fields as follows:

- FMModel
-- dims : Dimension of the factorization machine
-- logCV : Path for the printout of the log file for the CV run
-- logTest : Path for the printout of the log file for the Test run
-- libFMBinary: Path to the libFMBinary
-- strItr : number of iterations for the program to run. Stored as a string.
-- globalBias : 1 ==> Use global bias in factorization machine. 1 by default.
-- oneWay : 1==> Use one way interactions in factorization machine. 1 by default.
-- initStd : The initial standard deviation for the MCMC optimization technique as specified by the user in config.py

-SVDModel
--numItr : Number of iterations for the training run
-- SVDBufferPath : Path to the svd_feature_buffer program
-- learningRate : Learning rate (\lambda) for the SGD optimization technique used in SVDFeature
-- regularizationItem : Regularization term for the item parameters
-- regularizationUser : Regularization term for the user parameters
-- regularizationGlobal : Regularization term for the global parameters
-- numFactor : Number of factors used in the model
-- activeType : Sets the SVDFeature active type parameter
-- modelOutPath : Folder where all of the .model files are kept
-- SVDFeatureBinary : Path to the SVDFeature binary
-- SVDFeatureInferBinary : Path to the SVDFeature Infer binary

These subclasses also share the following methods:

- setup : Sets up the model dataset to be ran
- setupFeatures : Builds the features
- run : Runs the model
- fixRun : Fixes the printout of the run (or runs the prediction part)

Additional helper methods are used for carrying out these procedures.


--logCV : Where the logfile for the CV run is saved (libFM)
--logTest : Where the logfile for the Test run is saved (libFM)
--configPath : Where the config file for the run is saved (SVDFeature)

Data Flow Note
-------------------------------------
The flows for the datasets for the setup phase are different between libFM and SVDFeature and should be noted. Both start with the boot datasets. libFM then immediately adds features, taking boot->feat. Then it converts it into the libFM sparse matrix as feat->tmp. Then it is converted into the libFM binaries as tmp->run for runtime.

SVDFeature on the otherhand is different. It starts with boot but it is first reindexed going boot->tmp. Then features are added tmp->feat. Then the datasets are converted to the sparse form and the buffers feat-run.

Feature-Engineering
-------------------------------------
To feature-engineer for this program, you simply need to add new options to the setupFeatures method of the respective model type. New featureSets can be used by putting in a conditional checking for a new string passed in through the models list in config. As an instance function, it has access to all instance variables, which includes all relevant dataset paths. If any other materials are needed, it is wise to pass them into the model by adding them as class attributes through the constructor.
