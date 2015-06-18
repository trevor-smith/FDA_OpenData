import os
import time

from pymongo import MongoClient
import nltk

#from settings import Settings
# DATASET_FILE = '/Users/pniessen/yelp/boston/boston2/yelp_boston_academic_dataset_updated/yelp_academic_dataset_review.json'
# MONGO_CONNECTION_STRING = "mongodb://localhost:27030/"
# REVIEWS_DATABASE = "Dataset_Challenge_Reviews"
# TAGS_DATABASE = "Tags"
# REVIEWS_COLLECTION = "Reviews"
# CORPUS_COLLECTION = "Corpus"

client = MongoClient()
# reviews_collection = client.dsbc.Dataset_Challenge_Reviews.reviews # create collection
# dataset_file = DATASET_FILE

#reviews_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.REVIEWS_DATABASE][
#    Settings.REVIEWS_COLLECTION]
#tags_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.TAGS_DATABASE][Settings.REVIEWS_COLLECTION]
labels_tags_collection = client.drugs.labels_tags
drug_labeling = client.drugs.drug_labeling

labels_cursor = drug_labeling.find()
labelsCount = labels_cursor.count()
# reviews_cursor.batch_size(1000)

stopwords = {}
with open('topics_labels/stopwords.txt', 'rU') as f:
    for line in f:
        stopwords[line.strip()] = 1

done = 0
start = time.time()

docs = []
cursor = drug_labeling.find({})
for i in cursor:
    docs.append(i['results'])

data = []
for i in docs:
    for j in i:
        try:
            row = []
            row.append(j['id'])
            row.extend(j['warnings'])
            data.append(row)
        except:
            pass

tagged_collection = {}

for label in data:
    words = []
    sentences = nltk.sent_tokenize(label[1].lower())

    for sentence in sentences:
        tokens = nltk.word_tokenize(sentence)
        text = [word for word in tokens if word not in stopwords]
        tagged_text = nltk.pos_tag(text)

        for word, tag in tagged_text:
            words.append({"word": word, "pos": tag})

    labels_tags_collection.insert({
        "id": label[0],
        "warnings": label[1],
        "words": words
    })

    done += 1
    if done % 100 == 0:
        end = time.time()
        os.system('cls')
        print 'Done ' + str(done) + ' out of ' + str(labelsCount) + ' in ' + str((end - start))
