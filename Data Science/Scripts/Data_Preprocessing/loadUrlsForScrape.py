import os
import pandas as pd

urlNeg = []
urlPos = []

with open('../../../../../aclImdb/train/urls_neg.txt') as f1:
    for line in f1:
        urlNeg.append(line[:-13])



with open('../../../../../aclImdb/train/urls_pos.txt') as f1:
    for line in f1:
        urlPos.append(line[:-13])

urlAll = urlNeg + urlPos
urlAll = list(dict.fromkeys(urlAll))

#print(str(len(urlPos)))
#print(str(len(urlNeg)))
#print(str(len(urlAll)))