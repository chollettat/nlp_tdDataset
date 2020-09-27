# imporations
import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
from nltk.stem import PorterStemmer
import nltk
nltk.download('punkt')
nltk.download('stopwords')

# read txt file in several lines
lines = tuple(open('smsspamcollection.txt', 'r'))

# def variables
res, stemList, hamList, spamList = [], [], [], []

# preprocessing on spamcollection
def preprocess(lines,res,stemList) : 

    for i in range(0,len(lines)) :
        res.append(lines[i].split("\t")) # split with ham/spam and message
        res[i][1] = res[i][1].lower().strip().translate(str.maketrans("","",string.punctuation)) # convert to lowercase and remove with spaces
        res[i][1] = re.sub(r'\d+','',res[i][1]) # remove numbers

    ## define stopwords##
    stop_words = stopwords.words('english') 
    stop_words.append("u") # add stopwords to the list
    stemmer = PorterStemmer()

    for i in range(0,len(lines)) :
        tokens = word_tokenize(res[i][1])
        stemList=[]
        res[i][1] = [word for word in tokens if not word in stop_words]   # remove stopwords
        for word in res[i][1] :
            if len(word) > 2 : # remove words with 2 or less caracters
                stemList.append(stemmer.stem(word))
        res[i][1] = stemList
    return res


# split res into 2 lists, 1 for spam, 1 for ham
def splitList(lines,res,spamList,hamList) :
    res = preprocess(lines,res,stemList)
    for i in range(0,len(lines)) :
        if res[i][0]=='spam':
            spamList.append(res[i])
        else : 
            hamList.append(res[i])
    return hamList, spamList

hamList,spamList = splitList(lines,res,spamList,hamList)

