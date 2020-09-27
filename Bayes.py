

# imporations
import math
import time
import re
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from nltk import stem
import nltk
#nltk.download('punkt')
#nltk.download('stopwords')

tmps1=time.clock()
 



def allValue(sdata): #tell the all possible value of each feature
    i=0
    allwords = []
    
    while i < len(sdata):
        if not (sdata[i] in allwords):
            allwords.append(sdata[i])
        i = i+1
    allwords.sort()
    return allwords

def getAllWords(data):
    words = []
    for i in range(len(data)):
        for j in range(len(data[i])):
            words.append(data[i][j])
    return words


def valueFrequency(allData,allUniqueWords): #Give all frequency of a feature list
    frequencyList = []
    data=[]
    for i in range(0,len(allData)):
        data.append(allData[i][1])
    
    data = getAllWords(data)
    for j in range(0,len(allUniqueWords)):
        frequencyList.append(0)

    for k in range(0,len(allUniqueWords)):
        frequencyList[k] = data.count(allUniqueWords[k])
    
    for j in range(0,len(allUniqueWords)):
        frequencyList[j] = frequencyList[j] / len(data)
    
    return frequencyList



def Bayes(data,allFrequencyWords,sFrequency,hFrequency,allValueS,allValueH,spamHamFrequency): #data is a list without the "p or e"
    sumS=0
    sumH=0
    
    
    for i in range(0,len(data)):
            for k in range(0,len(allValueS)):
                if data[i] ==  allValueS[k]:
                    sumS = sumS + math.log(sFrequency[k])

            for k in range(0,len(allValueH)):
                if data[i] == allValueH[k]:
                    sumH = sumH + math.log(hFrequency[k])
    resS = math.log(spamHamFrequency[0]) + sumS
    resH = math.log(spamHamFrequency[1]) + sumH
    if resS<resH:
        return "spam"
    else : return "ham"


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




def probaSpamHam(data):

    res=[0,0]
    for i in range(len(data)):
        if data[i][0]=='spam':
            res[0] = res[0]+ 1
        else : 
            res[1] = res[1] + 1
    res[0] = res[0] / len(data)
    res[1] = res[1] / len(data)
    return res
    
    


def getAllUniqueWords(liste):
    sList =[]
    for i in range(0,len(liste)):
        sList.append(liste[i][1])
    allwords = getAllWords(sList)
    listWords = allValue(allwords)
    return listWords

def accuracyPrediction(listpredicted,listData):#Give  the precision of the modelPrediction
    acc = 0
    for i in range(0,len(listpredicted)):
        if listpredicted[i]==listData[i]:
            acc = acc + 1

    print(acc)
    acc = acc / len(listpredicted)

    return acc

def precisionPrediction(listpredicted,listData,label):#Give  the precision of the modelPrediction
    TP = 0
    FP =0
    for i in range(0,len(listpredicted)):
        if listpredicted[i]==listData[i]==label:
            TP = TP + 1
        if (listpredicted[i]==label and listData[i] != label):
            FP = FP +1
    res = TP / (TP + FP)

    return res

def recallPrediction(listpredicted,listData,label):
    TP = 0
    FN = 0
    for i in range(0,len(listpredicted)):
        if listpredicted[i]==listData[i]==label:
            TP = TP + 1
        if (listpredicted[i]!=label and listData[i] == label):
            FN = FN +1
    res = TP / (TP + FN)

    return res

def F1Score(precision,recall):
    return 2*(recall*precision)/(recall+precision)


def getTrainData(allData):
    trainData=[]
    for i in range(0,int(len(allData)*0.7)):
        trainData.append(allData[i])
    return trainData

def getTestData(allData):
    testData=[]
    for i in range(int(len(allData)*0.7),len(allData)):
        testData.append(allData[i])
    return testData


trainData = getTrainData(res)
testData = getTestData(res)
print(len(res),len(trainData),len(testData))
#print(getAllUniqueWords(hamList))
#print(valueFrequency(hamList,getAllUniqueWords(hamList)))

# hUniqueWords = getAllUniqueWords(hamList)
# sUniqueWords = getAllUniqueWords(spamList)
# aUniqueWords = getAllUniqueWords(res)

# spamHamFrequency= probaSpamHam(res)
# hFrequency= valueFrequency(hamList,hUniqueWords)
# sFrequency= valueFrequency(spamList,sUniqueWords)
# allFrequency= valueFrequency(res,aUniqueWords)

# predictedList = []
# valueList = [] #We want just spam or ham from the list



# for i in range(0,len(res)):
#     predictedList.append(Bayes(res[i][1],allFrequency,sFrequency,hFrequency,sUniqueWords,hUniqueWords,spamHamFrequency))
#     valueList.append(res[i][0])


# precHam = precisionPrediction(predictedList,valueList,"ham")
# precSpam = precisionPrediction(predictedList,valueList,"spam")
# recallHam = recallPrediction(predictedList,valueList,"ham")
# recallSpam = recallPrediction(predictedList,valueList,"spam")

# print("Accuracy : ",accuracyPrediction(predictedList,valueList))
# print("Precision on ham :", precHam)
# print("Precision on spam :", precSpam)
# print("recall on ham :", recallHam)
# print("recall on spam :",recallSpam)
# print("F1Score on ham",F1Score(precHam,recallHam))
# print("F1Score on spam",F1Score(precSpam,recallSpam))

# tmps2=time.clock()
# print ("Temps d'execution en secondes = " ,(tmps2-tmps1))