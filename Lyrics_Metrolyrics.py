import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import json_lines
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from collections import Counter
from sklearn.datasets import make_classification
from imblearn.combine import SMOTETomek
from imblearn.over_sampling import RandomOverSampler, SMOTE
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, f1_score
from wordcloud import WordCloud, STOPWORDS
from PIL import Image

# Insert lyrics location
df = pd.read_json (',lines=True)

# Feature Engineering
list_artists = ['Ed Sheeran','Camila Cabello','Queen','Eminem','Drake','Post Malone','Khalid','Rihanna']
df = df.drop(axis=0,labels=range(8))
df = df.reset_index()
df= df.drop(['index'],axis=1)
df = df.drop_duplicates(subset='lyrics')
df['artist'] = df[df['artist'].isin(list_artists)]
df = df.dropna()

### Train-test split
X = df['lyrics']
y = df['artist']
Xtrain, Xtest, ytrain, ytest = train_test_split(X,y)

## Convert Lyrics series to list
corpus = Xtrain.tolist()
corpus = [x.replace('\n', '') for x in corpus]
corpus = pd.Series(corpus)
tfidf = TfidfVectorizer()
dftf2 = tfidf.fit_transform(corpus)

# Naive Bayes
### MultinomialNB ###
nb = MultinomialNB(fit_prior=True)
nb.fit(dftf2, ytrain)
Xtest_trans = tfidf.transform(Xtest)
ypred = nb.predict(Xtest_trans)

### RandomOverSampler ###
ros = RandomOverSampler()
X_ros, y_ros = ros.fit_resample(dftf2,ytrain)
nb_ov = MultinomialNB()
nb_ov.fit(X_ros,y_ros)
ypred_ros = nb_ov.predict(Xtest_trans)

### SMOTETomek ###
smt = SMOTETomek()
Xsmt, ysmt = smt.fit_resample(dftf2,ytrain)
nb_smt = MultinomialNB()
nb_smt.fit(Xsmt,ysmt)
ypred_smt = nb_smt.predict(Xtest_trans)

### Comparison ###
all = plt.figure(figsize=(30, 7))

plt.subplot(131)
plt.hist(ypred,color='b',bins=30)
plt.hist(ytest,histtype='step',bins=30,color='r',stacked=True)
plt.xlabel('artists')
plt.ylabel('songs')
plt.title('MultinomialNB')
plt.subplot(132)
plt.hist(ypred_ros,color='b',bins=30)
plt.hist(ytest,histtype='step',color='r',bins=30,stacked=True)
plt.xlabel('artists')
plt.ylabel('songs')
plt.title('RandomOverSampler')
plt.subplot(133)
plt.hist(ypred_smt,color='b',bins=30,stacked=True)
plt.hist(ytest,histtype='step',color='r',bins=30)
plt.xlabel('artists')
plt.ylabel('songs')
plt.title('SMOTETomek')
plt.show()
