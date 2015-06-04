##### THIS FILE IS FOR DATA ANALYSIS #####

### IMPORTS ###
from pymongo import MongoClient
import pandas as pd
import numpy as np
import matplotlib as plt

### SETTING UP ENVIRONMENT ###
client = MongoClient()
labels = client.drugs.drug_labeling

### QUERYING THE DATA ###
# this would find all data...I have not given it any filters
cursor = labels.find({})

# this is just pulling the first document out of the database
# and then appending it to a list called 'documents'
# 'documents' will be a list of dictionaries
documents = []
for i in cursor[:20]:
    documents.append(i['results'])

# the elements of the 'documents' list are in fact dictionaries
# need to split them
data = []
for i in documents:
    for j in i:
        data.append(j)

### BASIC DATA ANALYSIS ###
df = pd.DataFrame(data)

# making our data strings because it is originally stored as a list
df.warnings = df.warnings.astype(str)

# # constructing tfidf matrix for each of our warning labels
# from sklearn.feature_extraction.text import TfidfVectorizer
# vectorizer = TfidfVectorizer(min_df=1, stop_words='english',ngram_range=(2,4))
# matrix = vectorizer.fit_transform(df.warnings)


# extracting length from warning label
from textblob import TextBlob


# extracting data from openfda dictionary
def clean_openfda_column():
    df['brand_name'] = df.openfda.apply(lambda x: x['brand_name'] if 'brand_name' in x else 'unknown')
    df['generic_name'] = df.openfda.apply(lambda x: x['generic_name'] if 'generic_name' in x else 'unknown')
    df['is_original_packager'] = df.openfda.apply(lambda x: x['is_original_packager'] if 'is_original_packager' in x else 'unknown')
    df['manufacturer_name'] = df.openfda.apply(lambda x: x['manufacturer_name'] if 'manufacturer_name' in x else 'unknown')
    df['nui'] = df.openfda.apply(lambda x: x['nui'] if 'nui' in x else 'unknown')
    df['package_ndc'] = df.openfda.apply(lambda x: x['package_ndc'] if 'package_ndc' in x else 'unknown')
    df['pharm_class_epc'] = df.openfda.apply(lambda x: x['pharm_class_epc'] if 'pharm_class_epc' in x else 'unknown')
    df['pharm_class_moa'] = df.openfda.apply(lambda x: x['pharm_class_moa'] if 'pharm_class_moa' in x else 'unknown')
    df['product_ndc'] = df.openfda.apply(lambda x: x['product_ndc'] if 'product_ndc' in x else 'unknown')
    df['product_type'] = df.openfda.apply(lambda x: x['product_type'] if 'product_type' in x else 'unknown')
    df['route'] = df.openfda.apply(lambda x: x['route'] if 'route' in x else 'unknown')
    df['rxcui'] = df.openfda.apply(lambda x: x['rxcui'] if 'rxcui' in x else 'unknown')
    df['spl_id'] = df.openfda.apply(lambda x: x['spl_id'] if 'spl_id' in x else 'unknown')
    df['spl_set_id'] = df.openfda.apply(lambda x: x['spl_set_id'] if 'spl_set_id' in x else 'unknown')
    df['substance_name'] = df.openfda.apply(lambda x: x['substance_name'] if 'substance_name' in x else 'unknown')
    df['unii'] = df.openfda.apply(lambda x: x['unii'] if 'unii' in x else 'unknown')
    df['upc'] = df.openfda.apply(lambda x: x['upc'] if 'upc' in x else 'unknown')
    df.product_type = df.product_type.astype(str)
    df.product_type = df.product_type.apply(lambda x: x.strip('['))
    df.product_type = df.product_type.apply(lambda x: x.strip(']'))

def textblob_features():
    df['polarity'] = df.warnings.apply(lambda x: TextBlob(x).polarity)
    df['subjectivity'] = df.warnings.apply(lambda x: TextBlob(x).subjectivity)
    df['length_of_warning'] = df.warnings.apply(lambda x: len(TextBlob(x).words))

def other_data_cleansing():
    df['date'] = pd.to_datetime(df.effective_time)

# running the cleaning
clean_openfda_column()
textblob_features()

### NLTK STUFF ###
# from __future__ import division
# import nltk
# from nltk import word_tokenize

# df.warnings = df.warnings.apply(lambda x: x.lower())
# df.tokens = df.warnings.apply(lambda x: word_tokenize(x))
# porter = nltk.PorterStemmer()
# df.stemmed = df.tokens.apply(lambda x: [porter.stem(t) for t in x])

# from sklearn.feature_extraction.text import CountVectorizer
# vectorizer = CountVectorizer(min_df=1, stop_words='english')
# matrix = vectorizer.fit_transform(df.warnings)



# # initial plotting
# df.length_of_warning.hist(bins=50)
# plt.show()

### WORKING WITH ADVERSE EVENTS ###

# getting data out of MongoDB
events = client.drugs.adverse_events
cursor = events.find({})

documents = []
for i in cursor:
    documents.append(i['results'])

data = []
for i in documents:
    for j in i:
        data.append(j)

# want to take a subset so I can start clustering
df_subset1 = df[['product_type', 'length_of_warning', 'polarity', 'subjectivity']]
print df_subset1.head(3)

df_subset1.drop('product_type', axis=1, inplace=True)

### CLUSTERING ###
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.preprocessing import StandardScaler

# preprocessing our data
# standard scalar...converts data into z scores
# this helps the clustering algorithms fit the data better

X = StandardScaler().fit_transform(df_subset1)

# ok, now to cluster with kmeans
# choosing 3 clusters first because the FDA gives 3 example tones (mild, moderate, severe)
num_clusters=3
km = KMeans(init='random', max_iter=100, n_init=1, verbose=1, n_jobs=-1, n_clusters=num_clusters)
km.fit(X)

# now to use dbscan
db = DBSCAN(eps=0.3, min_samples=10).fit(X)
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

print('Estimated number of clusters: %d' % n_clusters_)

# ok, this says 8 clusters...let's re-fit kmeans

num_clusters=8
km = KMeans(init='random', max_iter=100, n_init=1, verbose=1, n_jobs=-1, n_clusters=num_clusters)
km.fit(X)




