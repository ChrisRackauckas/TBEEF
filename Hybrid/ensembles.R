args<-commandArgs(TRUE)
trainPath = args[1]
CVPath    = args[2]
testPath  = args[3]
predCV    = args[4]
predTest  = args[5]
RMSEPath  = args[6]
model.type= args[7]
input1      = args[8]

library(Metrics)

dataTrain = read.csv(trainPath, sep="\t")
dataCV    = read.csv(CVPath,    sep="\t")
dataTest  = read.csv(testPath,  sep="\t")

if(model.type=="OLS"){
  ## Ordinary Least Squares
  library(ipred)
  fit      = lm(y~0 + .,data=dataTrain)
  summary(fit)
  CVPredictions = predict(fit,dataCV)
  TestPredictions= predict(fit,dataTest)
}

if(model.type=="OLSI"){
  ## Ordinary Least Squares with interaction terms
  library(ipred)
  formula = paste("y~0 + (.)^",input1,sep="")
  fit      = lm(y~0 + (.)^2,data=dataTrain)
  summary(fit)
  CVPredictions = predict(fit,dataCV)
  TestPredictions= predict(fit,dataTest)
}

if(model.type=="RR"){
  ## Ridge Regression
  library(ipred)
  library(ridge)
  input1 = as.numeric(input1)
  fit = linearRidge(y~0+.,data=dataTrain,nPCs=input1)
  print(fit)
  print("Ridge lambdas")
  print(fit$lambda)
  CVPredictions = predict(fit,dataCV)
  TestPredictions= predict(fit,dataTest)
}

if(model.type=="Lasso"){
  ## Lasso Regression
  library(glmnet)
  y = data.matrix(dataTrain$y)
  drops = c("y")
  x = data.matrix(dataTrain[,!(names(dataTrain) %in% drops)])
  fit = cv.glmnet(x,y)
  dataCVMat = data.matrix(dataCV[,!(names(dataCV) %in% drops)])
  CVPredictions = predict(fit,dataCVMat)
  TestPredictions= predict(fit,as.matrix(dataTest))
}

if(model.type=="BRT"){
  library(ipred)
  ## Bagged Regression Trees
  fit      = bagging(y~0+.,data=dataTrain)
  print(fit)
  CVPredictions = predict(fit,dataCV)
  TestPredictions= predict(fit,dataTest)
}

if(model.type=="BMAR"){
  library(BMA)
  ## Bayesian Model Averaging Regression
  y = dataTrain$y
  drops = c("y")
  x = dataTrain[,!(names(dataTrain) %in% drops)]
  fit      =  bicreg(x, y)
  summary(fit)
  cvp = predict(fit,dataCV)
  tp  = predict(fit,dataTest)
  CVPredictions   = unlist(cvp[1])
  TestPredictions = unlist(tp[1] )
}


if(model.type=="RFR"){
  library(randomForest)
  ## Random Forest
  fit      = randomForest(y ~0+., data=dataTrain,importance=TRUE, ntree=100)
  CVPredictions = predict(fit,dataCV)
  TestPredictions= predict(fit,dataTest)
}

if(model.type=="CIRF"){
  ## Conditional Inference Random Forest
  library(party)
  fit <- cforest(y ~ 0 + ., data = dataTrain)
  CVPredictions = predict(fit,dataCV)
  TestPredictions= predict(fit,dataTest)
}

if(model.type=="GBRT"){
  ## Gradient Boosted Regression Tree
  library(mboost)
  input1 = as.numeric(input1)
  fit <- blackboost(y ~ 0+., data = dataTrain,control = boost_control(mstop = input1))
  cv10f <- cv(model.weights(fit), type = "kfold")
  cvm <- cvrisk(fit)
  print(cvm)
  mstop(cvm)
  fit <- blackboost(y ~ 0+., data = dataTrain,control = boost_control(mstop = mstop(cvm)))
  CVPredictions = predict(fit,dataCV)
  TestPredictions= predict(fit,dataTest)
}

error=rmse(dataCV$y,CVPredictions)
print(error)

write(CVPredictions, file = predCV, ncolumns=1)
write(TestPredictions, file = predTest, ncolumns=1)
write(error,file=RMSEPath,ncolumns=1)