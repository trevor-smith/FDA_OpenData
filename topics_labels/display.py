import logging

from gensim.models import LdaModel
from gensim import corpora


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

dictionary_path = "topics_labels/models/dictionary.dict"
corpus_path = "topics_labels/models/corpus.lda-c"
lda_num_topics = 25
lda_model_path = "topics_labels/models/lda_model_50_topics.lda"

dictionary = corpora.Dictionary.load(dictionary_path)
corpus = corpora.BleiCorpus(corpus_path)
lda = LdaModel.load(lda_model_path)

topics = [5,10,15,20,25]
for num_topics in topics:
	print "number of topics:", num_topics
	i = 0
	for topic in lda.show_topics(num_topics):
	    print '#' + str(i) + ': ' + topic
	    i += 1

