def runModels(sys,os,utils,mproc,config):
    import modelFMRun
    for model in utils.modelsData:
        if model[1] == 'FM':
            modelFMRun.FMRun(os,utils,mproc,config,model)        
