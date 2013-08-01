import sys
def reIndex_Implicit(fin):#, fout):
    print("Reindexing Origin Data Set and Buiding the Correspondence Dics")
    fi = open( fin, 'r' ) #training set
    #fo = open( fout, 'w') #reindexed training set
    #extract from input file
    uidDic={}
    iidDic={}
    newuid=1
    newiid=1
    ctr=0  # is the counter of the total number.
    sum=0.0

    for line in fi:
        arr = line.split()
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
            
    #    fo.write('%d\t%d\t%d\n' %(uidDic[uid],iidDic[iid],rating))
    #fo.close()
    fi.close()
    #calculate different parameter.
    avg=sum/ctr
    #switch the key and the value in both dictionaries
    uidCorrespondence={value:key for key,value in uidDic.items()}
    iidCorrespondence={value:key for key,value in iidDic.items()}
    print("finished")
    return(uidCorrespondence,iidCorrespondence,avg)
    
def translate(fin,fout,Udic,ItemDic):
    print("start translation.Tranlating " +fin+" .")
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
    print("translation finished.")

def userfeedback(fname):
    fi = open(fname,'r')
    feedback = {}
    for line in fi:
        attr = line.strip().split('\t')
        uid = int(attr[0])-1
        iid = int(attr[1])-1
        if feedback.has_key(uid):
            feedback[uid].append(iid)
        else:
            feedback[uid] = [iid]
    fi.close()
    return feedback

#group num and order of the grouped training data
def usergroup(fname):
    fi = open(fname,'r')
    userorder = []
    groupnum = {}
    lastuid = -1
    for line in fi:
        attr = line.strip().split('\t')
        uid = int(attr[0])-1
        if groupnum.has_key(uid):
            groupnum[uid] += 1
        else:
            groupnum[uid] = 1
        if uid != lastuid:
            userorder.append(uid)
        lastuid = uid
    fi.close()
    return userorder,groupnum

#make implict feedback feature, one line for a user, wihch is in the order of the grouped training data 
#the output format:rate \t number of user group \t number of user implicit feedback \t fid1:fvalue1, fid2:fvalue2 ... \n
def mkfeature(fout,userorder,groupnum,feedback):
    fo = open(fout,'w')
    for uid in userorder:
        gnum = groupnum[uid]
        fnum = len(feedback[uid])
        fo.write('%d\t%d\t' %(gnum,fnum))
        for i in feedback[uid]:
            fo.write('%d:%.6f ' %(i,pow(fnum,-0.5)))
        fo.write('\n')

def mkImplicitFeatureFile(ftrain,fgtrain,fout):
    '''usage:<training_file> <grouped training_file> <output>'''
    feedback = userfeedback(ftrain)
    userorder,groupnum = usergroup(fgtrain)
    #make features and print them  out in file fout 
    mkfeature(fout,userorder,groupnum,feedback)
