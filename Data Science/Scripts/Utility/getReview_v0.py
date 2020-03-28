import pandas as pd

results = pd.read_csv("../Data/Results/results.csv")
#results['isNeg'] = to_numeric(results['isNeg'])

#results['isNeg'] = int(results['isNeg'])
#print(results.head())

print('Movie examples tt0064354, tt0100680, tt0047200')

movieName = input('Enter a movie id: ')
print('Results for: '+movieName)

query = results[results['movieName'] == movieName]
query = query.astype({'isNeg': int})
count = query.groupby('movieName').count()
summ = query.groupby('isNeg').count()

#print(results[results['movieName'] == movieName])
#print(str(summ.iloc[0][0]))
#print(str(count.iloc[0][0]))

print("Movie review summary: "+str(int(summ.iloc[0][0])/int(count.iloc[0][0])*100)[:5]+"% of the movie review are negative")