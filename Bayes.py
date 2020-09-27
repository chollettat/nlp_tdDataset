# Imporations
import math
import time
import re
import string
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from nltk.stem import PorterStemmer, WordNetLemmatizer

import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


# Preprocessing on spamCollection
def preprocess(lines,res,stemList) : 

    for i in range(0,len(lines)) :
        res.append(lines[i].split("\t")) # Split with ham/spam and message
        res[i][1] = res[i][1].lower().strip().translate(str.maketrans("","",string.punctuation)) # Convert to lowercase and remove with spaces
        res[i][1] = re.sub(r'\d+','',res[i][1]) # Remove numbers

    ## Define stopwords ##
    stop_words = stopwords.words('english') 
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()


    for i in range(0,len(lines)) :
        tokens = word_tokenize(res[i][1])
        stemList=[]
        lemList=[]
        res[i][1] = [word for word in tokens if not word in stop_words]   # remove stopwords
        for word in res[i][1] :
            if len(word) > 2 : # remove words with 2 or less caracters
                stemList.append(stemmer.stem(word))
        res[i][1] = stemList
        for word in res[i][1] : 
                lemList.append(lemmatizer.lemmatize(word))
        res[i][1] = lemList
    return res


#split res into 2 lists, 1 for spam, 1 for ham
def splitList(lines,res,spamList,hamList) :
    res = preprocess(lines,res,stemList)
    trainData = getTrainData(res)
    testData = getTestData(res)
    for i in range(0,len(trainData)) :
        if trainData[i][0]=='spam':
            spamList.append(res[i])
        else : 
            hamList.append(res[i])
    return hamList, spamList, trainData, testData


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


def allValue(data): # Tell the all differents words in all mail
    """
    data is a [list of string]. list of string is the different words in a mail. it's our data

    it returns a list of string, a list of unique word
    """
    i=0
    allwords = []
    
    while i < len(data):
        if not (data[i] in allwords):
            allwords.append(data[i])
        i = i+1
    allwords.sort()
    return allwords

def getAllWords(data): # Transform a list of list of string into a list of string, Which means merging all mail together
    """
    data is a [list of string]. list of string is the different words in a mail. it's our data

    it returns a list of string, a list of word

    """
    words = []
    for i in range(len(data)):
        for j in range(len(data[i])):
            words.append(data[i][j])
    return words


def getAllUniqueWords(data):# Give all unique words in our data
    """
    data is a list [ham or spam, [list of string]]. list of string is the different words in a mail. it's our data

    it returns a list of string, list of unique words
    """
    liste =[]
    for i in range(0,len(data)):
        liste.append(data[i][1]) # Transform shape of data
    allwords = getAllWords(liste)
    listWords = allValue(allwords)
    return listWords


def probaSpamHam(data): # Give the frequency of Ham mails and Spam mails
    """
    data is a list [ham or spam, [list of string]]. list of string is the different words in a mail. it's our data

    it returns a list of float, [frequency of spam, frequency of ham]

    """

    res=[0,0]
    for i in range(len(data)):
        if data[i][0]=='spam':
            res[0] = res[0]+ 1
        else : 
            res[1] = res[1] + 1
    res[0] = res[0] / len(data)
    res[1] = res[1] / len(data)
    return res

def valueFrequency(allData,allUniqueWords): # Give frequency for each unique words 
    """
    allData is a list [ham or spam, [list of string]]. list of string is the different words in a mail. it's our data
    allUniqueWords is a list of unique words of our data

    it returns a list of float,  the frequency for each unique word
    """
    frequencyList = []
    data=[]
    for i in range(0,len(allData)): # Transform shape of data 
        data.append(allData[i][1])
    
    data = getAllWords(data)
    for j in range(0,len(allUniqueWords)): 
        frequencyList.append(0)

    for k in range(0,len(allUniqueWords)):
        frequencyList[k] = data.count(allUniqueWords[k]) # We count each unique words 
    
    for j in range(0,len(allUniqueWords)):
        frequencyList[j] = frequencyList[j] / len(data) # We get the frequency by diving by all words 
    
    return frequencyList



def bayes(data,allFrequencyWords,sFrequency,hFrequency,allValueS,allValueH,spamHamFrequency): # This is our model prediction
    """
    Data is a list of words in a mail
    allFrequencyWords is a list of float which contains frequency of all unique words in our data
    sFrequency (hfrequency) is a list of float which contains frequency only for spam (ham) data
    allValueS (allValueH) is a list of unique words only for spam (ham) data
    spamHamFrequency is a list which contains the frequency of Spam and Ham in the data

    it returns a string, the predicted data
    """
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



    

def accuracyPrediction(listpredicted,listData):# Give  the accuracy of the modelPrediction
    """
    listpredicted is a list of string, containing only "ham" or "spam" predicted by bayes
    listData is a list of string, containg only "ham" or "spam" in our actual data

    it returns a float, the accuracy of our model
    """
    acc = 0
    for i in range(0,len(listpredicted)):
        if listpredicted[i]==listData[i]:
            acc = acc + 1

    acc = acc / len(listpredicted)

    return acc

def precisionPrediction(listpredicted,listData,label):# Give  the precision of the modelPrediction
    """
    listpredicted is a list of string, containing only "ham" or "spam" predicted by bayes
    listData is a list of string, containg only "ham" or "spam" in our actual data

    it returns a float, the precision of our model
    """

    TP = 0
    FP =0
    for i in range(0,len(listpredicted)):
        if listpredicted[i]==listData[i]==label: # We get the  True Positive
            TP = TP + 1
        if (listpredicted[i]==label and listData[i] != label): # We get the  False Positive
            FP = FP +1
    res = TP / (TP + FP)

    return res

def recallPrediction(listpredicted,listData,label):# Give the recall
    """
    listpredicted is a list of string, containing only "ham" or "spam" predicted by bayes
    listData is a list of string, containg only "ham" or "spam" in our actual data

    it returns a float, the recall of our model
    """
    TP = 0
    FN = 0
    for i in range(0,len(listpredicted)):
        if listpredicted[i]==listData[i]==label: # We get the  True Positive
            TP = TP + 1
        if (listpredicted[i]!=label and listData[i] == label):# We get the  False Negative
            FN = FN +1
    res = TP / (TP + FN)

    return res

def F1Score(precision,recall): # Give the F1Score
    """
    precision and recall are both float

    it returns a float, the F1Score of our model
    """
    return 2*(recall*precision)/(recall+precision)


stemList = []
def main():
    tmps1=time.process_time()
    # Read txt file in several lines
    lines = tuple(open('smsspamcollection.txt', 'r'))

    # Def variables
    res, hamList, spamList = [], [], []
    hamList,spamList,trainData,testData = splitList(lines,res,spamList,hamList) # Spam and ham lists are in the train data
    hUniqueWords = getAllUniqueWords(hamList)# We get unique words from hame
    sUniqueWords = getAllUniqueWords(spamList)# We get unique words from spam
    aUniqueWords = getAllUniqueWords(trainData)# We get all unique words

    spamHamFrequency= probaSpamHam(trainData) # We get frequencies of ham and spam
    hFrequency= valueFrequency(hamList,hUniqueWords) # we get frequencies from ham
    sFrequency= valueFrequency(spamList,sUniqueWords) # We get frequencies from spam
    allFrequency= valueFrequency(trainData,aUniqueWords) # We get frequencies for all words

    predictedList = []
    valueList = [] # We want just spam or ham from the list



    for i in range(0,len(testData)):
        predictedList.append(bayes(testData[i][1],allFrequency,sFrequency,hFrequency,sUniqueWords,hUniqueWords,spamHamFrequency)) # res[i][1] is the test data
        valueList.append(testData[i][0])


    precHam = precisionPrediction(predictedList,valueList,"ham") # Precision for ham
    precSpam = precisionPrediction(predictedList,valueList,"spam")# Precision for Spam
    recallHam = recallPrediction(predictedList,valueList,"ham") # Recall for ham
    recallSpam = recallPrediction(predictedList,valueList,"spam")# Recall for spam

    print("Accuracy : ",accuracyPrediction(predictedList,valueList)) # Accuracy for our model
    print("Precision on ham :", precHam)
    print("Precision on spam :", precSpam)
    print("recall on ham :", recallHam)
    print("recall on spam :",recallSpam)
    print("F1Score on ham",F1Score(precHam,recallHam)) # F1Score for ham
    print("F1Score on spam",F1Score(precSpam,recallSpam)) # F1Score for spam

    tmps2=time.process_time()
    print ("Executiuon time in secondes = " ,(tmps2-tmps1)) # Execution time

main()