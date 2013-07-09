def SVDSetup(os,utils,model,config):
    ### Take input to feat ###
    SVDSetupFeatures(os,utils,model)
    ### Take feat to tmp  to run ###
    # Need to finish: Correct inputs
    # Add tmp to run part
    values = SVDDataConvert(os,model[4][3],model[4][4],model[4][5],
                            model[4][6],model[4][7],model[4][8],
                            model[4][9],model[4][10],model[4][11],
                            utils.SVDFEATURE_BUFFER_BINARY)
    ### Write config file ###
    SVDWriteConfig(os,model,config,values)

def SVDSetupFeatures(os,utils,model):
    if model[2] == 'Basic':
        os.system('cp ' + model[4][0] + ' ' + model[4][3])
        os.system('cp ' + model[4][1] + ' ' + model[4][4])
        os.system('cp ' + model[4][2] + ' ' + model[4][5])

def SVDDataConvert(os,featTrain,featCV,featTest,tmpTrain,tmpCV,tmpTest,runTrain,runCV,runTest,SVDBufferPath):
    featTrainFile = open(featTrain, 'r')
    featCVFile    = open(featCV   , 'r')
    featTestFile  = open(featTest , 'r')
    tmpTrainFile  = open(tmpTrain,  'w')
    tmpTestFile   = open(tmpTest,   'w')
    tmpCVFile     = open(tmpCV,     'w')

    ############## Write tmp file reindexed ###############3
    trainLines = featTrainFile.readlines()
    CVLines    = featCVFile.readlines()
    testLines  = featTestFile.readlines()

    fullInput = []
    fullInput.append(trainLines)
    fullInput.append(CVLines)
    fullInput.append(testLines)

    uidDic={}
    iidDic={}
    newuid=1
    newiid=1
    ctr=0  # is the counter of the total number.
    sum=0.0

    #Build dictionary
    
    for line in trainLines:
        arr = line.rsplit('\t')
        uid = int(arr[0].strip())
        iid = int(arr[1].strip())
        rating = int(float(arr[2].strip()))
        #this part for calculating the average
        sum+=rating
        ctr+=1

		#this part for reindexing the user ID
        if uid not in uidDic:
            uidDic[uid]=newuid
            newuid+=1
		#this part for reindexing the item ID
        if iid not in iidDic:
            iidDic[iid]=newiid
            newiid+=1
    
    for line in CVLines:
        arr = line.rsplit('\t')
        uid = int(arr[0].strip())
        iid = int(arr[1].strip())
        #this part for reindexing the user ID
        if uid not in uidDic:
            uidDic[uid]=newuid
            newuid+=1
		#this part for reindexing the item ID
        if iid not in iidDic:
            iidDic[iid]=newiid
            newiid+=1
    
    for line in testLines:
        arr = line.rsplit('\t')
        uid = int(arr[0].strip())
        iid = int(arr[1].strip())
	    #this part for reindexing the user ID
        if uid not in uidDic:
            uidDic[uid]=newuid
            newuid+=1
		#this part for reindexing the item ID
        if iid not in iidDic:
            iidDic[iid]=newiid
            newiid+=1

    #Re-index
    for line in featTrainFile.readlines():
        arr = line.split()
        uid = int(arr[0].strip())
        iid = int(arr[1].strip())
        rating = int(float(arr[2].strip()))
        tmpTrainFile.write('%d\t%d\t%d\n' %(uidDic[uid],iidDic[iid],rating))
    for line in featCVFile.readlines():
        arr = line.split()
        uid = int(arr[0].strip())
        iid = int(arr[1].strip())
        tmpCVFile.write('%d\t%d\t%d\n' %(uidDic[uid],iidDic[iid]))
    for line in featTestFile.readlines():
        arr = line.split()
        uid = int(arr[0].strip())
        iid = int(arr[1].strip())
        tmpTestFile.write('%d\t%d\t%d\n' %(uidDic[uid],iidDic[iid]))
 
	#calculate different parameter.
    numUser=len(uidDic)
    numMovie=len(iidDic)
    avg=sum/ctr
	
    #Close files
    featTrainFile.close()
    featTestFile.close()
    featCVFile.close()
    tmpTrainFile.close()
    tmpTestFile.close()
    tmpCVFile.close()
	
    ############ tmp file is reindexed #####################
    ############ converting tmp to run binary buffer #######

    os.system(SVDBufferPath + ' ' + tmpTrain + ' ' + runTrain)
    os.system(SVDBufferPath + ' ' + tmpCV    + ' ' + runCV   )
    os.system(SVDBufferPath + ' ' + tmpTest  + ' ' + runTest )

    return (numUser,numMovie,avg)

def SVDWriteConfig(os,model,config,values):
    tag       = model[0]
    numGlobal = 0 #Change this
    numUser   = values[0]
    numMovie  = values[1]
    avg       = values[2]
    runTrain  = model[4][9]
    runCV     = model[4][10]
    runTest   = model[4][11]
    configCV  = model[4][15]
    configTest= model[4][16]

    for part in ['CV','Test']:
        if type == 'CV' :
            fout =  open(configCV,'w')
        else :
            fout =  open(configTest,'w')
        fout.write('#Config file for ' + tag + '\n')
        fout.write('#Global Bias\n')
        fout.write('base_score = '    + str(avg) + '\n')
        fout.write('#Learning Rate for SGD\n')
        fout.write('learning_rate = ' + config.SVD_LEARNING_RATE + '\n')
        fout.write('Regularization Constants (\lambda)\n')
        fout.write('wd_item = '       + config.SVD_REGULARIZATION_ITEM + '\n')
        fout.write('wd_user = '       + config.SVD_REGULARIZATION_USER + '\n')
        fout.write('wd_global = '     + config.SVD_REGULARIZATION_GLOBAL+'\n')
        fout.write('#Numbers of Features\n')
        fout.write('num_item = '      + str(numMovie) + '\n')
        fout.write('num_user = '      + str(numUser)  + '\n')
        fout.write('num_global = '    + str(numGlobal)+ '\n')
        fout.write('#Number of features\n')
        fout.write('num_feactor = '   + config.SVD_NUM_FACTOR + '\n')
        fout.write('#Translation function: 0=linear, 2=sigmoid\n')
        fout.write('active_type = '   + config.SVD_ACTIVE_TYPE + '\n')
        fout.write('#Prediction dataset\n')
        if type == 'CV':
            fout.write('test:buffer_feature = ' + runCV  + '\n')
        else :
            fout.write('test:buffer_feature = ' + runTest+ '\n')
        fout.write('#Training dataset\n')
        fout.write('buffer_feature = ' + runTrain + '\n')
        fout.close()
