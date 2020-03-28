import os
import pandas as pd

datasetPos = pd.DataFrame()
directoryPos = os.fsencode('../../../aclImdb/train/pos/')

for fileNamePos in os.listdir(directoryPos):
    with open('../../../aclImdb/train/pos/'+str(fileNamePos)[2:-1]) as f:
        review = f.read()
    datasetPos = pd.concat([datasetPos,pd.DataFrame(data={'filename': [str(fileNamePos)[2:-1]], 'review' : [review], 'id' : [int(str(fileNamePos)[2:str(fileNamePos).index('_')])]})])
    f.close()

datasetPos.sort_values(by=['id'], inplace=True)
datasetPos = datasetPos.reset_index()
print(datasetPos.head())


urlPos = []

with open('../../../aclImdb/train/urls_pos.txt') as f1:
    for line in f1:
        urlPos.append(line)

urlFramePos = pd.DataFrame({'url' : urlPos }) 
print(urlFramePos.head())

#pd.merge(dataset,urlFrame,on='')
finalDataSetPos = pd.concat([datasetPos, urlFramePos], axis=1)
finalDataSetPos['movieName'] = finalDataSetPos['url'].str[26:35]
print(finalDataSetPos)