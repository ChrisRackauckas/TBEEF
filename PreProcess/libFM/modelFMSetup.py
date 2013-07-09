def FMSetup(os,utils,model):
    import FMFeatureSetup
    ### Take boot to feat ###
    print("Setting Up Features")
    FMFeatureSetup.FMSetupFeatures(os,utils,model)
    ### Take feat to bin to run ###
    print("Converting Data")
    FMDataConvert(os,model)

def FMDataConvert(os,model):
#-----------------------------
# Takes in the raw data from original
# Makes the .libfm sparse matrix
# Then converts it to the binary form
#-----------------------------
    tag = model[0]
    featTrain = model[4][3]
    featCV    = model[4][4]
    featTest  = model[4][5]
    tmpTrain  = model[4][6]
    tmpCV     = model[4][7]
    tmpTest   = model[4][8]
    runTrain  = model[4][9]
    runCV     = model[4][10]
    runTest   = model[4][11]

    os.system('perl Models/libFM/triple_format_to_libfm.pl -in ' + 
            featTrain  + ',' + 
            featTest + ',' + 
            featCV + 
            ' -target 2 -separator \"\\t\"')
    os.system('./Models/libFM/convert --ifile ' + 
            featTrain + 
            '.libfm ' + '--ofilex ' + 
            tmpTrain + 
            '.x --ofiley ' + 
            runTrain + '.y' +
            '> /dev/null') 
    os.system('./Models/libFM/convert --ifile ' + 
            featCV + 
            '.libfm ' + '--ofilex ' + 
            tmpCV +
            '.x --ofiley ' + 
            runCV + '.y' +
            '> /dev/null')
    os.system('./Models/libFM/convert --ifile ' + 
            featTest + 
            '.libfm ' + '--ofilex ' + 
            tmpTest + 
            '.x --ofiley ' + 
            runTest + '.y'
            '> /dev/null')
    os.system('./Models/libFM/transpose --ifile ' + 
            tmpTrain + 
            '.x --ofile ' + 
            runTrain + '.xt' +
            '> /dev/null')
    os.system('./Models/libFM/transpose --ifile ' + 
            tmpTest + 
            '.x --ofile ' + 
            runTest + '.xt' +
            '> /dev/null')
    os.system('./Models/libFM/transpose --ifile ' + 
            tmpCV + '.x --ofile ' + 
            runCV + '.xt' + 
            '> /dev/null')  


