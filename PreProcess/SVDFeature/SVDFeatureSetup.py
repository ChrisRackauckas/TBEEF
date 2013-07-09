def SVDSetupFeatures(os,utils,model):
    if model[2] == 'Basic':
        basicConvert(model[4][6],model[4][3])
        basicConvert(model[4][7],model[4][4])
        basicConvert(model[4][8],model[4][5])

def basicConvert( fin, fout):
    fi = open( fin , 'r' )
    fo = open( fout, 'w' )
    #extract from input file    
    for line in fi:
        arr  =  line.split()               
        uid  =  int(arr[0].strip())
        iid  =  int(arr[1].strip())
        score=  int(arr[2].strip())
        fo.write( '%d\t0\t1\t1\t' %score )
        # Print data,user and item features all start from 0
        fo.write('%d:1 %d:1\n' %(uid-1,iid-1))
    fi.close()
    fo.close()
