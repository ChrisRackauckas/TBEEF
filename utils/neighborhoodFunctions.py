import sys
#This function is going to use the original training set, original movie set and original prediction set as input
#The TrainFile is in format of "uid \t mid \t rating"
#The PredFile is in format of "uid \t mid \t rating"
#The MovieTagFile is in format of "mid \t tag1,tag2,......."
#The CVFile is in format of "uid \t mid \t rating"
#For output
#The TrainFileReindex is in formate of "uid \t mid \t rating", with reindexed
#The PredFileReindex is in format of "uid \t mid \t rating",with reindexed
#The MovieTagFileReindex is in format of "mid \t tag1,tag2,.......", with reindexed
#The CVFileReindex is in format of "uid \t mid \t rating",with reindexed 
def reIndex(fin,gin,hin,CVfin,fout,gout,hout,CVfout):
    print("Run Neighborhood Model, Start Reindexing")

    TrainFile           =open(fin,'r')
    MovieTagFile        =open(gin,'r')
    PredFile            =open(hin,'r')
    CVFile              =open(CVfin,'r')
    TrainFileReindex    =open(fout,'w')
    MovieTagFileReindex =open(gout,'w')
    PredFileReindex     =open(hout,'w')
    CVFileReindex       =open(CVfout,'w')

    uidDic={}	#Key is original uid. Corresponding value is reindexed uid
    midDic={}	#Key is original mid. Corresponding value is reindexed mid
    tidDic={}	#Key is original tid. Corresponding value is reindexed tid
    mtlDic={}	#Key is mid.          Correspongding value is a list of the movie's tags

    newuid=0
    newmid=0
    newtid=0
    ctr   =0    #ctr keep the number of rating in training file.
    sum   =0    #sum up all the ratings in the training file
#this part is for reindexing trainfile
    for line in TrainFile:
        arr=line.split()
        uid=int(arr[0].strip())
        mid=int(arr[1].strip())
        rating=int(float(arr[2].strip()))
        sum +=rating
        ctr += 1
    
        if uid not in uidDic:
            uidDic[uid]=newuid
            newuid+=1

        if mid not in midDic:
            midDic[mid]=newmid
            newmid+=1

        TrainFileReindex.write('%d\t%d\t%d\n' %(uidDic[uid],midDic[mid],rating))

#this part is for reindexing CVfile
    for line in CVFile:
        arr=line.split()
        uid=int(arr[0].strip())
        mid=int(arr[1].strip())
        rating=int(float(arr[2].strip()))
    
        if uid not in uidDic:
            uidDic[uid]=newuid
            newuid+=1

        if mid not in midDic:
            midDic[mid]=newmid
            newmid+=1

        CVFileReindex.write('%d\t%d\t%d\n' %(uidDic[uid],midDic[mid],rating))


#this part is for reindexing predicting file	
    for line in PredFile:
        arr=line.split()
        uid=int(arr[0].strip())
        mid=int(arr[1].strip())
        rating=int(float(arr[2].strip()))
    
        if uid not in uidDic:
            uidDic[uid]=newuid
            newuid+=1

        if mid not in midDic:
            midDic[mid]=newmid
            newmid+=1

        PredFileReindex.write('%d\t%d\t%d\n' %(uidDic[uid],midDic[mid],rating))


#this part is for reindexing movie-tag file
    for line in MovieTagFile:
        arr=line.split()
        mid=int(arr[0].strip())
    
        if mid in midDic:
            Tag=(arr[1].strip())
            mtlDic[midDic[mid]]=list()
            TagList=Tag.split(',')

            for tid in TagList:
                if tid not in tidDic:
                    tidDic[tid]=newtid
                    newtid+=1
                mtlDic[midDic[mid]].append(tidDic[tid])

            MovieTagFileReindex.write(str(midDic[mid])+'\t')
            for tag in mtlDic[midDic[mid]]:
                MovieTagFileReindex.write(str(tag))
                if tag !=mtlDic[midDic[mid]][-1]:
                    MovieTagFileReindex.write(',')

            MovieTagFileReindex.write('\n')


    noUser =len(uidDic)
    noMovie=len(midDic)
    avg    =sum/ctr

    TrainFileReindex.close()
    MovieTagFileReindex.close()
    PredFileReindex.close()
    CVFileReindex.close()
    TrainFile.close()
    MovieTagFile.close()
    PredFile.close()
    CVFile.close()
    print("Reindexing Finished")
    return(noUser,noMovie,avg)

#This function is going to use movie_tag_new.txt to get movie pairs which have certain number of tags in common
#The input is movie-tag file(after reindexing). The format is "mid \t tag1,tag2,...."
#The output is in the format of "mid1 \t mid2 \t" Here the mid1 and mid 2 shares enough number of tags in common
def share(fin,fout):
    print("Generating Share Tag Files.")

    fi=open(fin,'r')
    fo=open(fout,'w')
    mtlDic={}

#this part is going to contruct the dictionary: movie id as key, and tag list as value	
    for line in fi:

        arr=line.split()
        mid=int(arr[0].strip())
        tag=(arr[1].strip())
        taglist=tag.split(',')
        
        mtlDic[mid]=list()		
    
        for tid in taglist:
            mtlDic[mid].append(tid)


#this part is for making the file of movie parirs which share enough number of tags
    for mid in mtlDic:
        for i in range(mid+1,len(mtlDic)+1):
            a_set=set(mtlDic[mid])
        
            if i in mtlDic:
                b_set=set(mtlDic[i])
                c_set=a_set.intersection(b_set)

            if len(c_set)>=10:
                fo.write('%s\t%s\n' %(mid,i))

    fo.close()
    fi.close()
    print("Generation Finished")

#This function is going to use user-movie-rating file (both training and testing set), sharing-tag movies pair file as input to get neighbourhoods sets for each given users and movies. 
#TrainingFile is in the format of "uid \t mid \t rating"
#ShareTag is in the format of "mid1 \t mid2"
#TeseFile is in the format of "uid \t mid \t rating"
def neighborhood(fin,gin,hin,fout,gout):
    print("Generating Neighborhood for" + ' ' + fin + ' and ' + hin + '.' )
    TrainingFile            =open(fin,'r')	#refers to the file of user-movie-rating training set
    ShareTag                =open(gin,'r')	#refers to the file of sharing-tag movie pair
    TestFile                =open(hin,'r')	#refers to the file of user-movie-rating test set
    TrainingFile_reformated =open(fout,'w')	#refers to the transfered format of training set
    TestFile_reformated     =open(gout,'w')	#refers to the transfered format of text set

    MovieNbhood={}			#refers to the dictionary of movie and a list which share tags with this movie
    UserMovieDic={}			#refers to the dictionary of user-movielist
    RatingDic={}			#refers to the dictionary of tuple of user-rating as a key and rating as a value
    AvgDic={}			    #refers to the dictionary of user and user's average rating
    IndexCorresDic={}		#refers to the dictionary of a scalar as a value and movie i and move j as key

#firstly, we make a dictionary of movie and a list inside which movies share tags with the key
    
    for line in ShareTag:
        arr=line.split()
        mid=int(arr[0].strip())
        MovNeighbor=int(arr[1].strip())

        if mid not in MovieNbhood:
            MovieNbhood[mid]=list()
            MovieNbhood[mid].append(MovNeighbor)
        else:
            MovieNbhood[mid].append(MovNeighbor)

#then, we get the dictionary of user-movielist and dictionary of tuple of user-rating as a key and rating as value and dictionary fo user and user's average rating  
    
    for line in TrainingFile:
        arr=line.split()
        uid=int(arr[0].strip())
        mid=int(arr[1].strip())
        rating=int(float(arr[2].strip()))
        RatingDic[(uid,mid)]=rating

        if uid not in UserMovieDic:
            UserMovieDic[uid]=list()
            UserMovieDic[uid].append(mid)
            AvgDic[uid]=rating
        else:
            AvgDic[uid]=(AvgDic[uid]*len(UserMovieDic[uid])+rating)/(len(UserMovieDic[uid])+1)
            UserMovieDic[uid].append(mid)
        
#now we get the neighborhood of training set
    
    b=0	#total no. of neighbors
    for uid in UserMovieDic:
        for mid in UserMovieDic[uid]:
            TrainingFile_reformated.write('%d\t' %RatingDic[(uid,mid)])
            a=0	#no. of neighbors of that particular movie
            a_list=list()
            if mid in MovieNbhood:			
                for movie in MovieNbhood[mid]:
                    if movie in UserMovieDic[uid]:	# if the user watched that movie in the neighborhood of the mid
                        b=b+1				
                        a=a+1						
                        c=RatingDic[(uid,movie)]-AvgDic[uid]	# c is the distance between rating and AVG
                        a_list.append(c)
                        IndexCorresDic[(mid,movie)]=b           # b is the index of the global feature.


                TrainingFile_reformated.write('%d\t1\t1\t' %a)
                for i in range(0,len(a_list)):
                    TrainingFile_reformated.write('%d:%f\t' %(b-a+i+1,a_list[i]))
                
                
            else:
                TrainingFile_reformated.write('0\t1\t1\t')
            TrainingFile_reformated.write('%d:1\t%d:1\n' %(uid,mid))
    

#the nwe get the neighborhood of testing set
    for line in TestFile:
        arr=line.split()
        uid=int(arr[0].strip())
        mid=int(arr[1].strip())
        rating=int(float(arr[2].strip()))			
        TestFile_reformated.write('%d\t' %rating)
        a=0		
        a_list=list()
        b_list=list()
        
        if mid in MovieNbhood and uid in UserMovieDic:
            for movie in MovieNbhood[mid]:
                if (mid,movie) in IndexCorresDic and movie in UserMovieDic[uid]:
                    c=RatingDic[(uid,movie)]-AvgDic[uid]
                    a_list.append(c)
                    m=IndexCorresDic[(mid,movie)]
                    b_list.append(m)
                    a=a+1
            TestFile_reformated.write('%d\t1\t1\t' %a)
            for i in range(0,len(a_list)):
                TestFile_reformated.write('%d:%f\t' %(b_list[i],a_list[i]))
        else:
            TestFile_reformated.write('0\t1\t1\t')
        TestFile_reformated.write('%d:1\t%d:1\n' %(uid,mid))
            
    TrainingFile.close()
    ShareTag.close()
    TestFile.close()
    TrainingFile_reformated.close()
    TestFile_reformated.close()
    print("Generation Finished")

    return(b)

