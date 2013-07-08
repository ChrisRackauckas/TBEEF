# This file is going to reindex the data of the baidu data set,it starts continuously from 1 to the total number of the data 

import sys

#make features,including global feature,user feature and item feature
#the input file format:userid \t itemid \t rate \n
#the output format:rate \t number of global features \t number of user features \t number of item features \t gfid:gfvalue ... ufid:ufvalue... ifid:ifvalue...\n
def setupBasic( fin, fout):
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
    print 'generation end'

def reIndex( fin, fout):
	fi = open( fin, 'r' )
	fo = open( fout, 'w')
	testfo= open('ua.test', 'w')
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
		fo.write('%d\t%d\t%d\n' %(uidDic[uid],iidDic[iid],rating))
		testfo.write('%d\t%d\n' %(uidDic[uid],iidDic[iid]))
	
	#calculate different parameter.
	noUser=len(uidDic)
	noMovie=len(iidDic)
	avg=sum/ctr
	print(noUser,noMovie)
	print("generation end, and the average is "+str(sum/ctr))

	fo.close()
	fi.close()
	return (noUser,noMovie,avg)
	
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('usage:<input> <output>')
        exit(-1)
    fin = sys.argv[1]
    fout = sys.argv[2]
    #make features and print them  out in file fout
    reIndex(fin,fout)
