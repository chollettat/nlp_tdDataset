
import matplotlib.pyplot as plt
from random import shuffle
from random import randrange
import math
import csv;


def readfile(filename):
    allData =[]
    fic = open("data.csv","r")
    file = fic.readlines()
    fic.close()
    removeLine(file)
    for k  in range(1,len(file)):
        allData.append(file[k].split(";")) # List of list, it has all the data. ( allData[i] is the number i data, allData[i][j] is the j feature of the i data

    shuffle(allData)   #shuffle the data

    return allData

def removeLine(file): #Remonve the \n of each line of the original data file
    i=0 
    while i < len(file):
        test = file[i]
        test = test.replace("\n","")
        
        file[i] = test
        i = i+1

def getNFeature(list,n):#take the n feature on each data
    i=0
    featureList= []
    while i<len(list) :
        featureList.append(list[i][n])
        i = i+1
        
    return featureList


        
def allValue(listFeature): #tell the all possible value of each feature
    i=0
    allFeatureValue = []
    while i < len(listFeature):
        if not (listFeature[i] in allFeatureValue):
            allFeatureValue.append(listFeature[i])
        i = i+1
    allFeatureValue.sort()
    return allFeatureValue



def valueFrequencyFeature(listFeature,allValue): #Give all frequency of a feature list
    allValueFeature = allValue
    frequencyList = []
    for j in range(0,len(allValueFeature)):
        frequencyList.append(0)

    for k in range(0,len(allValueFeature)):
        frequencyList[k] = listFeature.count(allValueFeature[k])
    
    for j in range(0,len(allValueFeature)):
        frequencyList[j] = frequencyList[j] / len(listFeature)
    
    return frequencyList

def frequencyData(data): #Give the frequency of a dataset
    allValueA=[]
    allFrequency =[]
    allFeature = []
    for i in range(0,len(data[0])):
        allFeature.append(getNFeature(data,i))
        allValueA.append(allValue(getNFeature(data,i)))
        allFrequency.append(valueFrequencyFeature(allFeature[i],allValueA[i]))
    return allValueA, allFrequency

def makeAllGraph(data,allValueF,allFrequency,name): #Make all graph for each feature
    for i in range(0,len(data[0])):
        plt.bar(allValueF[i],height=allFrequency[i],width=0.5)
        plt.title(name[i])
        plt.savefig(name[i] +".png")
        plt.cla()

def splitData(data):#split the list onto 2 lists. on the first one there is onlu edibledata, et poisondata on the second one. It helps calculating P(Xi|Y)
    p = []
    e = []
    for i in range(0,len(data)):
        if data[i][12] == "Yes":
            p.append(data[i])
        else : 
            e.append(data[i])

    return p,e


def kLaplaceSmoothing(edibleFrequency,poisonFrequency,pEdible,pPoison,k): #transform all data frequency onto a Laplace Smoothing frequency (i don't know but it doesn't work)
    i=1
    eF=edibleFrequency
    pF = poisonFrequency
    while i<len(edibleFrequency):
        n = len(edibleFrequency[i])
        for j in range(0,n):
            eF[i][j] = (float(edibleFrequency[i][j]) + float(k))/(float(pEdible)+ (float(n)*float(k)))
        i = i+1
    i=1
    while i<len(poisonFrequency):
        n = len(poisonFrequency[i])
        for j in range(0,n):
            pF[i][j] = (float(poisonFrequency[i][j]) + float(k))/(float(pPoison)+ (float(n)*float(k)))
        i = i+1
    return pF,eF

def modelPrediction(data,allFrequency,poisonFrequency,edibleFrequency,allValueA,allValueP,allValueE): #data is a list without the "p or e"
    sumP=0
    sumE=0
    res=[]
    
    for i in range(0,len(data)):
        if not "?" in allValueA[i+1]:
            for k in range(0,len(allValueE[i+1])):
                if data[i]==allValueE[i+1][k]:
                    sumE = sumE + math.log(edibleFrequency[i+1][k])
            for k in range(0,len(allValueP[i+1])):
                if data[i]==allValueP[i+1][k]:
                    sumP = sumP + math.log(poisonFrequency[i+1][k])
    resE=math.log(allFrequency[0][0]) + sumE
    resP=math.log(allFrequency[0][1]) + sumP

    if resE>resP:
        return "No"
    else : return "Yes"

def precisionPrediction(listpredicted,listData):#Give  the precision of the modelPrediction
    acc = [0,0]
    for i in range(0,len(listpredicted)):
        if listpredicted[i]==listData[i]:
            acc[0] = acc[0] + 1
        else :
            acc[1] = acc[1] +1
    acc[0] = acc[0] / len(listpredicted)
    acc[1] = acc[1] / len(listpredicted)
    return acc

def cross_validation_split(dataset, n_folds):
	dataset_split = list()
	dataset_copy = list(dataset)
	fold_size = int(len(dataset) / n_folds)
	for _ in range(n_folds):
		fold = list()
		while len(fold) < fold_size:
			index = randrange(len(dataset_copy))
			fold.append(dataset_copy.pop(index))
		dataset_split.append(fold)
	return dataset_split

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

allData = readfile("data.csv");

def main():
    a=4
   
    allRes =[]
    tmpRes = 0
    accuracy =0
    allData=[]
    allData=readfile('readfile.csv')
    datasplit = cross_validation_split(allData,a) #split the data using cross splt

    for k in range(len(datasplit)):
        trainData= getTrainData(datasplit[k])
        testData= getTestData(datasplit[k]);

        yData, nData = splitData(trainData)

        #for graph
        name = ['Age knowing No','Sexe knowing No','Siblings knowing No','Social Class knowing No','Futur of Earth knowing No','Heterosexual knowing No','Divorced Parent knowing No','House or Appartement knowing No','Heartbreak knowing No','In relationship knowing No','Friends with childs knowing No','Living with parents knowing No','WANT CHILDRENS BEFORE 30YO knowing No']
        #nameE = ['edible Data','cap-shape-givenE','cap-surface-givenE','cap-coulor-givenE','bruises-givenE','odor-givenE','gill-attachement-givenE','gill-spacing-givenE','gill-size-givenE','gill-color-givenE','stalk-shape-givenE','stalk-root-givenE','stalk-surface-above-ring-givenE','stalk-surface-below-ring-givenE','stalk-color-above-ring-givenE','stalk-color-below-ring-givenE','veil-type-givenE','veil-color-givenE','ring-number-givenE','ring-type-givenE','spore-print-color-givenE','population-givenE','habitat-givenE']

        allValueA,frequencyAll = frequencyData(trainData)
        allValueY,frequencyYes = frequencyData(yData)
        allValueN,frequencyNo= frequencyData(nData)

        #q=["b","f","n","t","a","a","c","b","k","e","b","f","f","n","n","p","n","n","c","k","a","g"] a single data test

        answer =[]
        answerL=[]
        testData = []

        pFreqLaplace,eFreqLaplace = kLaplaceSmoothing(frequencyNo,frequencyYes,frequencyAll[0][0],frequencyAll[0][1],20) #laplace smoothing

        allValueA,frequencyAll = frequencyData(trainData)
        allValueY,frequencyYes = frequencyData(yData)
        allValueN,frequencyNo= frequencyData(nData)

        #all,frequency = frequencyData(allData)
        makeAllGraph(nData,allValueN,frequencyNo,name)

        #makeAllGraph(poisonData,allValueP,frequencyPoison,nameP)
        #makeAllGraph(edibleData,allValueE,frequencyEdible,nameE)
        #If you want to create graph


        

        for i in range(0,len(trainData)):#Make the prediction
            j=1
            tmp=[]
            while j <len(trainData[i]):
                tmp.append(trainData[i][j]) 
                j=j+1
            testData.append(tmp)
            answer.append(modelPrediction(testData[i],frequencyAll,frequencyYes,frequencyNo,allValueA,allValueY,allValueN))
            answerL.append(modelPrediction(testData[i],frequencyAll,pFreqLaplace,eFreqLaplace,allValueA,allValueY,allValueN))



        acc = precisionPrediction(answer,getNFeature(allData,12))#accuracy of the model without laplace smoothing
        allRes.append(acc)
        #accLaplace = precisionPrediction(answerL,getNFeature(allData,12))#accuracy of the model withlaplace smoothing
        print("this is the accuracy of the prediction model without Laplace smoothing",acc)
        #print("the fist one is the ration of good prediction, false for the seconde")
        #print("this is the accuracy of the prediction model with Laplace smoothing",accLaplace)

    for i in range(a):
           tmpRes = allRes[i][0]+tmpRes
    accuracy =  tmpRes/k
    print("the mean accuracy is :",accuracy)

main()



#for i in range(0,len(trainData)):#Make the prediction
#            j=1
#            tmp=[]
#            while j <len(trainData[i]):
#                tmp.append(trainData[i][j]) 
#                j=j+1
#            testData.append(tmp)
#            answer.append(modelPrediction(testData[i],frequencyAll,frequencyYes,frequencyNo,allValueA,allValueY,allValueN))
#            answerL.append(modelPrediction(testData[i],frequencyAll,pFreqLaplace,eFreqLaplace,allValueA,allValueY,allValueN))    

#def main():
#    allData=[]
#    allData=readfile('readfile.csv')
#    trainData= getTrainData(allData);
#    testData= getTestData(allData);
#    yData, nData = splitData(trainData)

#    #for graph
#    name = ['Age','Sexe','Siblings','Social Class','Futur of Earth','Heterosexual','Divorced Parent','House or Appartement','Heartbreak','In relationship','Friends with childs','Living with parents','WANT CHILDRENS BEFORE 30YO']
#    #nameE = ['edible Data','cap-shape-givenE','cap-surface-givenE','cap-coulor-givenE','bruises-givenE','odor-givenE','gill-attachement-givenE','gill-spacing-givenE','gill-size-givenE','gill-color-givenE','stalk-shape-givenE','stalk-root-givenE','stalk-surface-above-ring-givenE','stalk-surface-below-ring-givenE','stalk-color-above-ring-givenE','stalk-color-below-ring-givenE','veil-type-givenE','veil-color-givenE','ring-number-givenE','ring-type-givenE','spore-print-color-givenE','population-givenE','habitat-givenE']

#    allValueA,frequencyAll = frequencyData(trainData)
#    allValueY,frequencyYes = frequencyData(yData)
#    allValueN,frequencyNo= frequencyData(nData)

#    #q=["b","f","n","t","a","a","c","b","k","e","b","f","f","n","n","p","n","n","c","k","a","g"] a single data test

#    answer =[]
#    answerL=[]
#    testData = []

#    pFreqLaplace,eFreqLaplace = kLaplaceSmoothing(frequencyNo,frequencyYes,frequencyAll[0][0],frequencyAll[0][1],20) #laplace smoothing

#    allValueA,frequencyAll = frequencyData(trainData)
#    allValueY,frequencyYes = frequencyData(yData)
#    allValueN,frequencyNo= frequencyData(nData)

#    all,frequency = frequencyData(allData)
#    makeAllGraph(allData,all,frequency,name)

#    #makeAllGraph(poisonData,allValueP,frequencyPoison,nameP)
#    #makeAllGraph(edibleData,allValueE,frequencyEdible,nameE)
#    #If you want to create graph

#    datasplit = cross_validation_split(allData,3) #split the data using cross splt
#    datasplit = cross_validation_split(allData,3) #split the data using cross splt
#    for k in range(len(datasplit)):

#        for i in range(0,len(datasplit[k])):#Make the prediction
#            j=1
#            tmp=[]
#            while j <len(datasplit[k][i]):
#                tmp.append(datasplit[k][i][j]) 
#                j=j+1
#            testData.append(tmp)
#            answer.append(modelPrediction(testData[i],frequencyAll,frequencyYes,frequencyNo,allValueA,allValueY,allValueN))
#            answerL.append(modelPrediction(testData[i],frequencyAll,pFreqLaplace,eFreqLaplace,allValueA,allValueY,allValueN))



#        acc = precisionPrediction(answer,getNFeature(allData,12))#accuracy of the model without laplace smoothing
#        #accLaplace = precisionPrediction(answerL,getNFeature(allData,12))#accuracy of the model withlaplace smoothing
#        print("this is the accuracy of the prediction model without Laplace smoothing",acc)
#        print("the fist one is the ration of good prediction, false for the seconde")
#        #print("this is the accuracy of the prediction model with Laplace smoothing",accLaplace)

   
#    print("ok")