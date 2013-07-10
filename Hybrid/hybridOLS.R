args<-commandArgs(TRUE)
trainPath = args[1]
CVPath    = args[2]
testPath  = args[3]
predCV    = args[4]
predTest  = args[5]

dataTrain = read.csv(trainPath, sep="\t")
dataCV    = read.csv(CVPath,    sep="\t")
dataTest  = read.csv(testPath,  sep="\t")
fit = lm(y~.,data=dataTrain)
summary(fit)
CVPredictions = predict(fit,dataCV)
TestPredictions= predict(fit,dataTest)
write(CVPredictions, file = predCV, ncolumns=1)
write(TestPredictions, file = predTest, ncolumns=1)