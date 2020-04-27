import pandas as pd
import nltk
from nltk.corpus import wordnet
import string
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.tokenize import WhitespaceTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from gensim.test.utils import common_texts
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, auc, roc_auc_score
import matplotlib.pyplot as plt
import pickle5 as pickle 
import joblib
import os
#from wordcloud import WordCloud
#import matplotlib.pyplot as plt

#load data
reviews_df = pd.read_csv("../Data/Training_Data/Train.csv")

#select a small number of rows to check
reviews_df = reviews_df.sample(frac = 0.01, replace = False, random_state=42)

reviews = reviews_df[["review", 'movieName']]
reviews = reviews.reset_index()
reviews_df["is_bad_review"] = reviews_df["isNeg"]
reviews_df = reviews_df[["review", "is_bad_review"]]
#print(reviews_df)

def get_wordnet_pos(pos_tag):
    if pos_tag.startswith('J'):
        return wordnet.ADJ
    elif pos_tag.startswith('V'):
        return wordnet.VERB
    elif pos_tag.startswith('N'):
        return wordnet.NOUN
    elif pos_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

def clean_text(text):
    text = text.lower()
    text = [word.strip(string.punctuation) for word in text.split(" ")]
    text = [word for word in text if not any(c.isdigit() for c in word)]
    stop = stopwords.words('english')
    text = [x for x in text if x not in stop]
    text = [t for t in text if len(t) > 0]
    pos_tags = pos_tag(text)
    text = [WordNetLemmatizer().lemmatize(t[0], get_wordnet_pos(t[1])) for t in pos_tags]
    text = [t for t in text if len(t) > 1]
    text = " ".join(text)
    return(text)

reviews_df["review_clean"] = reviews_df["review"].apply(lambda x: clean_text(x))

sid = SentimentIntensityAnalyzer()
reviews_df["sentiments"] = reviews_df["review"].apply(lambda x: sid.polarity_scores(x))
reviews_df = pd.concat([reviews_df.drop(['sentiments'], axis=1), reviews_df['sentiments'].apply(pd.Series)], axis=1)

reviews_df["nb_chars"] = reviews_df["review"].apply(lambda x: len(x))
reviews_df["nb_words"] = reviews_df["review"].apply(lambda x: len(x.split(" ")))

documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(reviews_df["review_clean"].apply(lambda x: x.split(" ")))]

model = Doc2Vec(documents, vector_size=5, window=2, min_count=1, workers=4)
doc2vec_df = reviews_df["review_clean"].apply(lambda x: model.infer_vector(x.split(" "))).apply(pd.Series)
doc2vec_df.columns = ["doc2vec_vector_" + str(x) for x in doc2vec_df.columns]
reviews_df = pd.concat([reviews_df, doc2vec_df], axis=1)

tfidf = TfidfVectorizer(min_df = 10)
tfidf_result = tfidf.fit_transform(reviews_df["review_clean"]).toarray()
tfidf_df = pd.DataFrame(tfidf_result, columns = tfidf.get_feature_names())
tfidf_df.columns = ["word_" + str(x) for x in tfidf_df.columns]
tfidf_df.index = reviews_df.index
reviews_df = pd.concat([reviews_df, tfidf_df], axis=1)

#reviews_df["is_bad_review"].value_counts(normalize = True)

#selecting feturees
label = "is_bad_review"
ignore_cols = [label, "review", "review_clean"]
features = [c for c in reviews_df.columns if c not in ignore_cols]

X_test = reviews_df[features]

print(X_test)

rfModel = joblib.load('sentimentModel.pkl')
y_pred = [x[1] for x in rfModel.predict_proba(X_test)]
print(y_pred)

results = pd.DataFrame(y_pred)
print(results)

predictions = pd.concat([reviews, results], axis=1)
predictions = predictions[predictions.columns[-2:]]
print(predictions)

if os.path.exists('../Data/Results/results_test.csv'):
    os.remove('../Data/Results/results_test.csv')
    print('File already exists \nDeletingFile...\nWriting file ../Data/Results/results_test.csv')
    predictions.to_csv(r'../Data/Results/results_test.csv')
else:
    predictions.to_csv(r'../Data/Results/results_test.csv')
    print('Data written to file in ../Data/Results/results_test.csv')

