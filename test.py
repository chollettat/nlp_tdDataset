# -*- coding: utf-8 -*-

#imports
import pandas as pd
from sklearn.model_selection import train_test_split

#read the file, split in 2 columns (ham/spam and comments)
datas = pd.read_csv('smsspamcollection.txt', sep="\t", header=None,converters={i: str for i in range(0,2)})
datas.to_csv('smsspamcollection.csv',index=None)
datas[0] = datas[0].map({'ham':0,'spam':1})
print(datas)
#split dataset 
train, test = train_test_split(datas, test_size=0.2, random_state=42, shuffle=True)
