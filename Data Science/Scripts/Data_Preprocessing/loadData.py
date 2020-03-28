import os
import pandas as pd

datasetNeg = pd.DataFrame()
directoryNeg = os.fsencode('../../../aclImdb/train/neg/')

for fileName in os.listdir(directoryNeg):
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

#----------------------------------------------------------------------------------------------------------------------------------------------------

datasetPos = pd.DataFrame()
directoryPos = os.fsencode('../../../aclImdb/train/pos/')

for fileName in os.listdir(directoryPos):
    with open('../../../aclImdb/train/pos/'+str(fileName)[2:-1]) as f:
        review = f.read()
    datasetPos = pd.concat([datasetPos,pd.DataFrame(data={'filename': [str(fileName)[2:-1]], 'review' : [review], 'id' : [int(str(fileName)[2:str(fileName).index('_')])]})])
    f.close()

datasetPos.sort_values(by=['id'], inplace=True)
datasetPos = datasetPos.reset_index()
print(datasetPos.head())


urlPos = []

with open('../../../aclImdb/train/urls_pos.txt') as f1:
    for line in f1:
        urlPos.append(line)

urlDFPos = pd.DataFrame({'url' : urlPos }) 
print(urlDFPos.head())

finalDataSetPos = pd.concat([datasetPos, urlDFPos], axis=1)
finalDataSetPos['movieName'] = finalDataSetPos['url'].str[26:35]
finalDataSetPos['isNeg'] = 0
print(finalDataSetPos)

#---------------------------------------------------------------------------------------------------------------------------------------------------

trainingDataset = finalDataSetNeg.append(finalDataSetPos)
print(trainingDataset)

if os.path.exists('../Data/Training_Data/Train.csv'):
    os.remove('../Data/Training_Data/Train.csv')
    print('File already exists \nDeletingFile...\nWriting file ../Data/Training_Data/Train.csv')
    trainingDataset.to_csv(r'../Data/Training_Data/Train.csv')
else:
    trainingDataset.to_csv(r'../Data/Training_Data/Train.csv')
    print('Data written to file in ../Data/Training_Data/Train.csv')