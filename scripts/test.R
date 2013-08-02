### This file can be used to easily test the ensemble models 
### It is recommended to be done interactively through the interpreter
### via something like Rstudio. This way you can run your R commands
### on the files to see what exactly happens in real time!

trainPath = "..Data/HybridSetup/boot_train_t0"
CVPath    = "..Data/HybridSetup/boot_CV_t0"
testPath  = "..Data/HybridSetup/orig_test_t0"
predCV    = "..Data/HybridPredictions/OLSR_CV_t0_tmp"
predTest  = "..Data/HybridPredictions/OLSR_test_t0_tmp"
dataTrain = read.csv(trainPath, sep="\t")
dataCV    = read.csv(CVPath,    sep="\t")
dataTest  = read.csv(testPath,  sep="\t")
library(ipred)





fit   = bagging(y~0+.,data=dataTrain)

fit = lm(y~0 + (.)^2,data=dataTrain)
summary(fit)

predict(fit,dataTest)
CVPredictions = predict(fit,dataCV)
TestPredictions= predict(fit,dataTest)

write(CVPredictions, file = predCV, ncolumns=1)
write(TestPredictions, file = predTest, ncolumns=1)

