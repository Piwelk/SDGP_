import os
import pandas as pd

reviews = pd.read_csv("../Data/Training_Data/Train.csv")
print(reviews.head())

reviewSummary = pd.read_csv("../Data/Training_Data/movieDetails.csv")
reviewSummary = reviewSummary[['movieName','summary']]
print(reviewSummary.head())

reviews = reviews[['movieName','review']]
reviews['review'] = reviews[['movieName','review']].groupby(['movieName'])['review'].transform(lambda x: ','.join(x))
reviews = reviews[['movieName','review']].drop_duplicates()
print(reviews.head())

training = pd.merge(reviews, reviewSummary, on='movieName')
print(training.head())

if os.path.exists('../Data/Training_Data/Train_v2.csv'):
    os.remove('../Data/Training_Data/Train_v2.csv')
    print('File already exists \nDeletingFile...\nWriting file ../Data/Training_Data/Train_v2.csv')
    training.to_csv(r'../Data/Training_Data/Train_v2.csv')
else:
    training.to_csv(r'../Data/Training_Data/Train_v2.csv')
    print('Data written to file in ../Data/Training_Data/Train_v2.csv')