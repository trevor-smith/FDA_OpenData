import os
import time

from pymongo import MongoClient
from nltk.stem.wordnet import WordNetLemmatizer

# #from settings import Settings
# DATASET_FILE = '/Users/pniessen/yelp/boston/boston2/yelp_boston_academic_dataset_updated/yelp_academic_dataset_review.json'
# MONGO_CONNECTION_STRING = "mongodb://localhost:27030/"
# REVIEWS_DATABASE = "Dataset_Challenge_Reviews"
# TAGS_DATABASE = "Tags"
# REVIEWS_COLLECTION = "Reviews"
# CORPUS_COLLECTION = "Corpus"


client = MongoClient()
labels_collection = client.drugs.labels # create collection
labels_tags_collection = client.drugs.labels_tags
labels_corpus_collection = client.drugs.labels_corpus

#tags_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.TAGS_DATABASE][Settings.REVIEWS_COLLECTION]
#corpus_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.TAGS_DATABASE][Settings.CORPUS_COLLECTION]



labels_cursor = labels_tags_collection.find()
labelsCount = labels_cursor.count()
labels_cursor.batch_size(5000)

lem = WordNetLemmatizer()

done = 0
start = time.time()

# docs = []
# cursor = enforcement.find({})
# for i in cursor:
#     docs.append(i['results'])
#
# data = []
# for i in docs:
#    	for j in i:
#    		data.append(j)

for label in labels_cursor:
    nouns = []
    words = [word for word in label["words"] if word["pos"] in ["NN", "NNS"]]

    for word in words:
        nouns.append(lem.lemmatize(word["word"]))

    try:
        labels_corpus_collection.insert({
            "id": label["id"],
            "warnings": label["warnings"],
            "words": nouns
        })

        done += 1
        if done % 100 == 0:
            end = time.time()
            os.system('cls')
            print 'Done ' + str(done) + ' out of ' + str(labelsCount) + ' in ' + str((end - start))
    except:
        pass
