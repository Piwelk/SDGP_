import os
import pandas as pd

reviews = pd.read_csv("../Data/Results/results.csv")
print(reviews.head())

reviewSummary = pd.read_csv("../Data/Results/movieDetails.csv")
#reviewSummary = reviewSummary[['movieName','summary']]
print(reviewSummary.head())

finalResults = pd.merge(reviews, reviewSummary, on='movieName')
print(finalResults.head())

if os.path.exists('../Data/Results/finalResults.csv'):
    os.remove('../Data/Results/finalResults.csv')
    print('File already exists \nDeletingFile...\nWriting file ../Data/Results/finalResults.csv')
    finalResults.to_csv(r'../Data/Results/finalResults.csv')
else:
    finalResults.to_csv(r'../Data/Results/finalResults.csv')
    print('Data written to file in ../Data/Results/finalResults.csv')