args<-commandArgs(TRUE)
trainPath = args[1]
CVPath    = args[2]
testPath  = args[3]
predCV    = args[4]
predTest  = args[5]
RMSEPath  = args[6]

library(ipred)
dataTrain = read.csv(trainPath, sep="\t")
dataCV    = read.csv(CVPath,    sep="\t")
dataTest  = read.csv(testPath,  sep="\t")
fit = lm(y~0 + .,data=dataTrain)
summary(fit)
errFit   = errorest(y~0+.,data=dataTrain,model=lm)
print(errFit)

error = errFit$error

CVPredictions = predict(fit,dataCV)
TestPredictions= predict(fit,dataTest)
write(CVPredictions, file = predCV, ncolumns=1)
write(TestPredictions, file = predTest, ncolumns=1)
write(error,file=RMSEPath,ncolumns=1)