args<-commandArgs(TRUE)
trainPath = args[1]
CVPath    = args[2]
testPath  = args[3]
predCV    = args[4]
predTest  = args[5]
RMSEPath  = args[6]
model.type= args[7]
misc      = args[8]

library(ipred)

dataTrain = read.csv(trainPath, sep="\t")
dataCV    = read.csv(CVPath,    sep="\t")
dataTest  = read.csv(testPath,  sep="\t")

if(model.type=="OLS"){
  ## Ordinary Least Squares
  ## Works
  fit      = lm(y~0 + .,data=dataTrain)
  errFit   = errorest(y~0+.,data=dataTrain,model=lm)
  summary(fit)
}

if(model.type=="OLSI"){
  ## Ordinary Least Squares in second order interactions
  ## Works
  fit      = lm(y~0 + (.)^2,data=dataTrain)
  errFit   = errorest(y~0+(.)^2,data=dataTrain,model=lm)
  summary(fit)
}

if(model.type=="RR"){
  ## Ridge Regression
  ## Works
  library(ridge)
  fit = linearRidge(y~0+.,data=dataTrain,nPCs=2)
  ridgeModel = function(formula, data) {
    mod <- linearRidge(formula, data=data,nPCs=2)
    function(newdata) predict(mod, newdata)
  }
  errFit   = errorest(y~0+.,data=dataTrain,model=ridgeModel)
  print(fit)
  print("Ridge lambdas")
  print(fit$lambda)
}

if(model.type=="BRT"){
  ## Bagged Regression Trees
  ## Works
  fit      = bagging(y~0+.,data=dataTrain)
  errFit   = errorest(y~0+.,data=dataTrain,model=bagging)
  print(fit)
}

if(model.type=="BMAR"){
  library(BMA)
  ## Bayesian Model Averaging Regression
  fit      =  bicreg(x, y, strict = FALSE, OR = 20)
}

if(model.type=="RF"){
  library(randomForest)
  ## Random Forest
  fit      = randomForest(y ~0+., data=dataTrain,importance=TRUE)
  errFit   = errorest(y~0+.,data=dataTrain,model=randomForest)
}

if(model.type=="CIRF"){
  ## Conditional Inference Random Forest
  library(party)
  library(languageR)
  data.controls <- cforest_unbiased(ntree=500, mtry=3)
  fit <- cforest(y ~ 0 + ., data = dataTrain, 
                          controls=data.controls) 
}

if(model.type=="GBRT"){
  ## Gradient Boosted Regression Tree
  library(mboost)
  fit <- blackboost(y ~ 0+., data = dataTrain,control = boost_control(mstop = 50))
  cv10f <- cv(model.weights(fit), type = "kfold")
  cvm <- cvrisk(fit)
  print(cvm)
  mstop(cvm)
  fit <- blackboost(y ~ 0+., data = dataTrain,control = boost_control(mstop = mstop(cvm)))
  errFit   = errorest(y~0+.,data=dataTrain,model=blackboost)
}

print(errFit)
error = errFit$error

CVPredictions = predict(fit,dataCV)
TestPredictions= predict(fit,dataTest)
write(CVPredictions, file = predCV, ncolumns=1)
write(TestPredictions, file = predTest, ncolumns=1)
write(error,file=RMSEPath,ncolumns=1)