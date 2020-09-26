# imporations
import re
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from nltk import stem
import nltk
nltk.download('punkt')
nltk.download('stopwords')

# read and split txt file in several lines
lines = tuple(open('smsspamcollection.txt', 'r'))
res, hamList, spamList = [], [],[]

for i in range(0,len(lines)) :
    res.append(lines[i].split("\t"))
    res[i][1] = res[i][1].lower()

    ###TESTS FOR FIND ANOTHER STOPWORDS###
    if res[i][0]=='spam':
        spamList.append(res[i])
    else : 
       hamList.append(res[i])

#res[i][1] = re.sub(r'\d+','',res[i][1])
#stemmer = stem.SnowballStemmer('english')
stop_words = stopwords.words('english')
#stop_words.append("go")

for i in range(0,len(lines)) :

  # remove stopwords
  tokens = word_tokenize(res[i][1])
  res[i][1] = [word for word in tokens if not word in stop_words]


print(hamList)
