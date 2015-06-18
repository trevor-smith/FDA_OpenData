import logging
import json

from gensim.models import LdaModel
from gensim import corpora
import nltk
from nltk.stem.wordnet import WordNetLemmatizer

import os
import time

from pymongo import MongoClient
import nltk


class Predict():
    def __init__(self):
        dictionary_path = "topics/models/dictionary.dict"
        lda_model_path = "topics/models/lda_model_55_topics.lda"
        self.dictionary = corpora.Dictionary.load(dictionary_path)
        self.lda = LdaModel.load(lda_model_path)

    def load_stopwords(self):
        stopwords = {}
        with open('topics/stopwords.txt', 'rU') as f:
            for line in f:
                stopwords[line.strip()] = 1

        return stopwords

    def extract_lemmatized_nouns(self, new_review):
        stopwords = self.load_stopwords()
        words = []

        sentences = nltk.sent_tokenize(new_review.lower())
        for sentence in sentences:
            tokens = nltk.word_tokenize(sentence)
            text = [word for word in tokens if word not in stopwords]
            tagged_text = nltk.pos_tag(text)

            for word, tag in tagged_text:
                words.append({"word": word, "pos": tag})

        lem = WordNetLemmatizer()
        nouns = []
        for word in words:
            if word["pos"] in ["NN", "NNS"]:
                nouns.append(lem.lemmatize(word["word"]))

        return nouns

    def run(self, new_review):
        nouns = self.extract_lemmatized_nouns(new_review)
        new_review_bow = self.dictionary.doc2bow(nouns)
        new_review_lda = self.lda[new_review_bow]

        return new_review_lda



def main():
    client = MongoClient()
    reviews = client.drugs.Corpus
    print "Number of documents in collection:", reviews.count()
    print "Sample entry:"
    counter = 0
    num_topics = 50

    for num in range(num_topics):
        weight_dict[num] = 0
        count_dict[num] = 0

    cursor = reviews.find(no_cursor_timeout=True)
    #print cursor.count()

    # keys = [u'text', u'reviewId', u'_id', u'business']
    # try:
    for item in cursor[:1]:
        # try:
        business_id = item[u'event_id']
        review_text = item[u'reason_for_recall']

        if business_id not in lda_dict:
            lda_dict[business_id] = {}
        #lda_dict[business_id][review_id] = review_text

        #logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

        predict = Predict()
        review_topic = predict.run(review_text)
        #print "review_topic:", review_topic

        lda_dict[business_id] = review_topic

        # log topic frequency / sum
        for topic in review_topic:
            print topic
            print type(topic)
            topic_num, value = topic
            weight_dict[topic_num] += value
            count_dict[0] +=1
            # print weight_dict
        counter = counter + 1
    print lda_dict


#         if counter % 1000 == 0:
#             print "counter:", counter

#         #         except:
#         #             print "error:", item
#         #             pass
#         # except:
#         #     print "error"
#         #     counter = counter +1
#         #     pass

#         # now save to file
#     basedir = '/Users/trevorsmith/Desktop/fda_topic_modeling/'
#     filename = 'reason_for_recall_lda_' + str(num_topics) + '_dict.json'
#     with open (basedir + filename, "wb") as f:
#         json.dump(lda_dict, f)
#     print filename, "written with", len(lda_dict), "elements"

#     print "There are", len(lda_dict), "busineses in lda_dict:"
#     keys = lda_dict.keys()
#     for key in keys:
#         print key,":", len(lda_dict[key]), "reviews"

#     weight = sorted(weight_dict.items(), key=lambda x: x[1], reverse = True)
#     count = sorted(count_dict.items(), key=lambda x: x[1], reverse = True)
#     print "sorted summed topic weights:", weight
#     print "sorted topic count:", count


# if __name__ == '__main__':
#     lda_dict = {}
#     weight_dict = {}
#     count_dict = {}

main()
