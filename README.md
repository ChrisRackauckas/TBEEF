TBEEF - Triple Bagged Ensemble Ensemble Framework
==============================================

This program is a hybrid recommendation system, an implementation of the TBEEF algorithm which utilizes various different statistical models and ensemble tehcniques, patching them together in an intelligent way to improve prediction accuracy. It was specifically developed to implement the methods from the various top competitors in the Baidu, Inc. movie recommendation algorithm contest into a single unified approach and is written to work with datasets which follow the format of the contest.

Program Structure
----------------------------------------------

The structure of the program is as follows. There are three main phases of the prediction algorithm:

1. Pre-Processing - Getting the data ready.
2. Model Setup - Building all of the features for running the models.
3. Modeling - Running the models to generate the predictions.
4. Hybrid Setup - Aggregating the predictions and setting up for the hybrid models.
5. Hybrid Modeling - Running multiple ensemble models
6. Synthesize - Aggregating of the ensemble models through gradient boosted regression
6. Post-Processing - Fixing predictions and finding which of the random trials had the lowest cross-validation RMSE.

This program requires two datasets: a training dataset and a test/prediction dataset. The training dataset is used to train the models and the prediction dataset is simply a file with predictors for which the program will generate predictions.

Contributors
----------------------------------------------

*	Chris Rackauckas, University of California, Irvine
*	Colin Jarvis, Macalester College
*	Weijie CAI, Hong Kong University of Science and Technology
*	Chenxiao XU, The Chinese University of Hong Kong

Acknowledgements
----------------------------------------------

This research was made possible through the Research Industrial Projects for Students, Hong Kong (RIPS-HK), an undergraduate research opportunity ran by UCLA's Institute for Pure and Applied Mathematics (IPAM). This project was funded by the NSF. We thank our academic mentor Dr. Avery Ching, Hong Kong University of Science and Technology, and our industry client Baidu, Inc. for helping guide us through the project.
