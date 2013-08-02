import sys
'''
Program input requirement:
    1.reIndex_Implicit: The format of fin should be UserID \t MovieID \t ratings \n
    2.translate:
        This function is to reindex the input file according to the correspondence Dictionaries from reIndex_Implicit function
        input file format:
            UserID \t MovieID \t [The third column is optional] \n
    3.userfeedback, usergroup and mkfeature are the functions called by mkImplicitFeatureFile. 
        input file format:
            the input file1 format of ftrain:  userid \t itemid \t rate \n
            the input file2 format of fgtrain: userid \t itemid \t rate \n, which is grouped by user
            the output format:                 rate \t number of user group \t number of user implicit feedback \t fid1:fvalue1, fid2:fvalue2 ... \n
'''

def reIndex_Implicit(ftrain,fCV,ftest,ftrainOut,fCVOut,ftestOut):
    print("Reindexing Data Sets and Building the Correspondence Dics")
    bootTrainFile = open(ftrain, 'r')
    bootCVFile    = open(fCV   , 'r')
    bootTestFile  = open(ftest , 'r')
    tmpTrainFile  = open(ftrainOut,  'w')
    tmpTestFile   = open(ftestOut,   'w')
    tmpCVFile     = open(fCVOut,     'w')

    ############# Write tmp file reindexed ###############3
    trainLines = bootTrainFile.readlines()
    CVLines    = bootCVFile.readlines()
    testLines  = bootTestFile.readlines()

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
    for line in trainLines:
        arr = line.split()
        uid = int(arr[0].strip())
        iid = int(arr[1].strip())
        rating = int(float(arr[2].strip()))
        tmpTrainFile.write('%d\t%d\t%d\n' %(uidDic[uid],iidDic[iid],rating))
    for line in CVLines:
        arr = line.split()
        uid = int(arr[0].strip())
        iid = int(arr[1].strip())
        rating = int(float(arr[2].strip()))
        tmpCVFile.write('%d\t%d\t%d\n' %(uidDic[uid],iidDic[iid],rating))
    for line in testLines:
        arr = line.split()
        uid = int(arr[0].strip())
        iid = int(arr[1].strip())
        rating = int(float(arr[2].strip()))
        tmpTestFile.write('%d\t%d\t%d\n' %(uidDic[uid],iidDic[iid],rating))

    avg=sum/ctr
    #Close files
    bootTrainFile.close()
    bootTestFile.close()
    bootCVFile.close()
    tmpTrainFile.close()
    tmpTestFile.close()
    tmpCVFile.close()
    print("Finished")
    return(uidDic,iidDic,avg)


def translate(fin,fout,Udic,ItemDic):
    print("Start Translation. Translating " +fin+" .")
    fi=open(fin,'r')
    fo=open(fout,'w')
    #translate the file
    for line in fi:
        arr=line.split()
        uid=int(arr[0].strip())
        iid=int(arr[1].strip())
        if len(arr)>2:
            rating=str(int(float(arr[2].strip())))
        if uid in Udic:
            if iid in ItemDic:
                if len(arr)>2:
                    writeline=str(Udic[uid])+'\t'+str(ItemDic[iid])+'\t'+rating+'\r\n'
                else:
                    writeline=str(Udic[uid])+'\t'+str(ItemDic[iid])+'\r\n'
                fo.write(writeline)

    fi.close()
    fo.close()
    print("Translation Finished.")

def userfeedback(fname):
    fi = open(fname,'r')
    feedback = {}
    for line in fi:
        attr = line.strip().split('\t')
        uid = int(attr[0])-1#uid actually start from 0
        iid = int(attr[1])-1#mid actually start from 0
        if uid in feedback:
            feedback[uid].append(iid)
        else:
            feedback[uid] = [iid]
    fi.close()
    return feedback

#usergroup function is to find out group num and order of user in the grouped training data file
def usergroup(fname):
    fi = open(fname,'r')
    userorder = []
    groupnum = {}
    lastuid = -1
    for line in fi:
        attr = line.strip().split('\t')
        uid = int(attr[0])-1   #uid actually start from 0
        if uid in groupnum:
            groupnum[uid] += 1
        else:
            groupnum[uid] = 1
        if uid != lastuid:
            userorder.append(uid)
        lastuid = uid
    fi.close()
    return userorder,groupnum


#mkfeature is  to calculate the parameters of the feadback features
def mkfeature(fout,userorder,groupnum,feedback):
    fo = open(fout,'w')
    for uid in userorder:
        gnum = groupnum[uid]
        fnum = len(feedback[uid])
        fo.write('%d\t%d\t' %(gnum,fnum))
        for i in feedback[uid]:
            fo.write('%d:%.6f ' %(i,pow(fnum,-0.5)))
        fo.write('\n')



#make implicit feedback features
def mkImplicitFeatureFile(ftrain,fgtrain,fout):
    feedback = userfeedback(ftrain)
    userorder,groupnum = usergroup(fgtrain)
    #make features and print them  out in file fout 
    mkfeature(fout,userorder,groupnum,feedback)
