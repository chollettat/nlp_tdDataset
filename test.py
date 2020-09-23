#imports
import pandas as pd
from sklearn.model_selection import train_test_split

#read the file, split in 2 columns (ham/spam and comments)
datas = pd.read_csv('smsspamcollection.txt', sep="\t", header=None)
#datas.columns = ["type","comments"]
print(datas[1])

#split dataset 
train, test = train_test_split(datas, test_size=0.2, random_state=42, shuffle=True)
