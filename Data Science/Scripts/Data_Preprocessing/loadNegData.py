import os
import pandas as pd

datasetNeg = pd.DataFrame()
directoryNeg = os.fsencode('../../../aclImdb/train/neg/')

for fileName in os.listdir(directoryNeg):
    print(fileName)
    with open('../../../aclImdb/train/neg/'+str(fileName)[2:-1]) as f:
        review = f.read()
    datasetNeg = pd.concat([datasetNeg,pd.DataFrame(data={'filename': [str(fileName)[2:-1]], 'review' : [review], 'id' : [int(str(fileName)[2:-7])]})])
    f.close()

datasetNeg.sort_values(by=['id'], inplace=True)
datasetNeg = datasetNeg.reset_index()
print(datasetNeg.head())


urlNeg = []

with open('../../../aclImdb/train/urls_neg.txt') as f1:
    for line in f1:
        urlNeg.append(line)

urlDFNeg = pd.DataFrame({'url' : urlNeg }) 
print(urlDFNeg.head())

#pd.merge(dataset,urlFrame,on='')
finalDataSetNeg = pd.concat([datasetNeg, urlDFNeg], axis=1)
finalDataSetNeg['movieName'] = finalDataSetNeg['url'].str[26:35]
finalDataSetNeg['isNeg'] = 1
print(finalDataSetNeg)