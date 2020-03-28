import os
import pandas as pd

url = []

with open('../../aclImdb/train/urls_neg.txt') as f1:
    for line in f1:
        url.append(line)

print(str(url))
urlDF = pd.DataFrame({'url' : url }) 

print(urlDF.head())