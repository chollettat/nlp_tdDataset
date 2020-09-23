import pandas as pd

X = pd.read_csv('smsspamcollection.txt', sep="\t", header=None)
print(X[1])