import pandas as pd

resultsSent = pd.read_csv("../Data/Results/results.csv")
results = pd.read_csv("../Data/Results/movieDetails.csv")
#results['isNeg'] = to_numeric(results['isNeg'])

#results['isNeg'] = int(results['isNeg'])
#print(results.head())

print('Movie examples Stanley & Iris, Robot Wars, Alive')

movieName = input('Enter a movie id: ')
print('Results for: '+movieName)
query = results[results['name'].str.contains(movieName)]

query1 = resultsSent[resultsSent['movieName'] == query.iloc[0]['movieName'].strip()]
query1 = query1.astype({'isNeg': int})
count = query1.groupby('movieName').count()
summ = query1.groupby('isNeg').count()

#print(results[results['movieName'] == movieName])
#print(str(summ.iloc[0][0]))
#print(str(count.iloc[0][0]))

print("\nMovie review summary: "+str(int(summ.iloc[0][0])/int(count.iloc[0][0])*100)[:5]+"% of the movie review are negative")

print('Name:    '+query.iloc[0]['name'])
print('Year:    '+str(query.iloc[0]['year']))
print('Rating:  '+str(query.iloc[0]['rating']))
print('Genre:   '+query.iloc[0]['genre'].strip())
print('Summary: '+query.iloc[0]['summary'].strip())
print('ID:      '+query.iloc[0]['movieName'].strip())