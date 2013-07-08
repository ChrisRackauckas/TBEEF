### Imports
library(ridge)
library(Metrics)

### Read in the data
dataTrain = read.csv("Data/Hybrid/hybridTrain.txt", sep="\t")
dataPredict = read.csv("Data/Hybrid/hybridPredict.txt", sep="\t")
actual = dataTrain$y

### Fit function

### Fit the model

rmseBest = 5
bestI = 0
lambdas = seq(0,10,.1)
for(i in 1:length(lambdas)){
  fit = linearRidge(y~.,data=dataTrain,lambda=lambdas[i])
  prediction = predict(fit,dataTrain)
  calc = rmse(actual,prediction)
  ## Saves first, second, and third so far
  if(calc<rmseBest){
    rmseBest=calc
    bestI=i
  }
}

print(rmseBest)
print(bestI)
fit = linearRidge(y~.,data=dataTrain,lambda=lambdas[bestI])
prediction =  predict(fit,dataCV)
write(predictions, file ="Data/Hybrid/hybridSynthesized.txt", ncolumns=1)