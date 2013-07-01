Hybrid Movie Recommendation System
==============================================

This program is a hybrid recommendation system, utilizing the models from various different statistical methods and patching them together in an intelligent way to improve prediction accuracy. It was specifically developed to implement the methods from the various top competitors in the Baidu, Inc. movie recommendation algorithm contest into a single unified approach and is written to work with datasets which follow the format of the contest.

Program Structure
----------------------------------------------

The structure of the program is as follows. There are three main phases of the prediction algorithm:

1. Pre-Processing - Getting the data ready to run the models.
2. Modeling - Running the models to generate the predictions.
3. Post-Processing - Utilizing the predictions from various models to generate a prediction.

This program requires three datasets: a training dataset, cross-validation dataset, and a test/prediction dataset. The training dataset is used to train the models and the cross-validation dataset is used to train the post-processing techniques. Lastly, it uses the trained model to output the predictions for the test dataset (and, if the test set has predictions, it will also output the RMSE on the test set).

The Pre-Processing stage contains two main files:

1. effects.py, a file which parses the input training and cross-validation set for global effects (global mean, user mean, movie mean, etc), re-scales the data to be mean zero, and save the global information out to Data/Effects/globalEffects.txt for use in the post-processing phase.

2. model$NAMESetup.py, a file which parses the de-globaled dataset for use within the specific named model. For example, modelFM.py would parse the training and cross-validation datasets into the binary forms for use in libFM and save these files to Data/ModelData/$NAME

The Modeling stage contains the following items:

1. The programs for training the models and outputting predictions, such as libFM, SVDFeature, etc.

2. model$NAMERun.py, a file which uses the data from Data/ModelData/$NAME to train the model and generates predictions which are saved to Data/ModelPredictions.

The Post-Processing stage contains two main files:

1. hybrid.py, a script which takes in the predictions from Data/ModelPredictions and uses them to generate the predictions.

2. post.py, a script which reformats the predictions by placing back in the global effects and looking for duplicates from the training set in the test set (and replacing with the appropriate value). It outputs the final predictions to Data/Outputs

For convenience, commonly used utility functions are stored in scripts within the utils folder.

ToDo
----------------------------------------------

1. Integrate libFM into the program
2. Integrate SVDFeature into the program
3. Develop a simple hybridization script
4. Write effects.py
5. Multi-thread the driver
6. Integrate post-processing pair finding replacement.

Acknowledgements
----------------------------------------------

This research was made possible through the Research Industrial Projects for Students, Hong Kong (RIPS-HK), an undergraduate research opportunity ran by UCLA's Institute for Pure and Applied Mathematics (IPAM). This project was funded by the NSF. We thank our academic mentor Dr. Avery Ching, Hong Kong University of Science and Technology, and our industry client Baidu, Inc. for helping guide us through the project.