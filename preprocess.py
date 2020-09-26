# imporations
import re
#from nltk.corpus import stopwords 
#from nltk.tokenize import word_tokenize 

# read and split txt file in several lines
lines = tuple(open('smsspamcollection.txt', 'r'))
res = []
test=True
nbSpamNumber, nbSpam, nbHamNumber, nbHam = 0, 0, 0, 0

for i in range(0,len(lines)) :
    res.append(lines[i].split("\t"))
    res[i][1] = res[i][1].lower()

    # remove stopwords
    #stop_words = set(stopwords.words('english'))
    #tokens = word_tokenize(res[i][1])
    #res[i][1] = [i for i in tokens if not i in stop_words]


    ###TESTS FOR FIND ANOTHER STOPWORDS###
    if res[i][0]=='spam':
        nbSpam+=1
        test=bool(re.search(r'\d',res[i][1]))
        if test==True :
            nbSpamNumber+=1
    else : 
        nbHam+=1
        print(type(res[i][1]))
        test=bool(re.search(r'\d',res[i][1]))
        if test==True :
            nbHamNumber+=1
            #res[i][1] = re.sub(r'\d+','',res[i][1])
    #print(res[i][1])

