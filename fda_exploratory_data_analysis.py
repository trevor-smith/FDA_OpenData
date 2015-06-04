##### THIS FILE IS FOR EXPLORATORY ANALYSIS #####

### IMPORTS ###
from pymongo import MongoClient
import pandas as pd
import numpy as np
import pprint
from collections import Counter
import matplotlib.pyplot as plt

### SETTING UP ENVIRONMENT ###
# make sure mongod is running
client = MongoClient()
labels = client.drugs.drug_labeling
events = client.drugs.adverse_events

### QUERYING THE DATA ###
# this would find all data...I have not given it any filters
cursor_labels = labels.find({})
cursor_events = events.find({})

# this is just pulling the mongodb documents out of the database
# and then appending it to a list called 'documents'
# 'documents' will be a list of dictionaries
documents_labels = []
for i in cursor_labels[:20]:
    documents_labels.append(i['results'])

documents_events = []
for i in cursor_events[:20]:
    documents_events.append(i['results
                            '])

# the elements of the 'documents' list are in fact dictionaries
# need to split them
data_labels = []
for i in documents_labels:
    for j in i:
        data_labels.append(j)

data_events = []
for i in documents_events:
    for j in i:
        data_events.append(j)


### CLEANING THE DATA ###
# flattening the nested dicts
import collections

def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))

    return dict(items)

for i in data_events[:5]:
    print "this person's sex is: " + str((i['patient']['patientsex']))
    for j in i['patient']['reaction']:
        print "this person had this type of reaction: " + str(j['reactionmeddrapt'])

cnt = Counter()
for i in data_events[:5]:
    for j in i['patient']['reaction']:
        cnt[j['reactionmeddrapt']] += 1

print cnt.most_common(10)

# we can do some basic plotting
# need to get the data out of the counter
top_10 = cnt.most_common(10)

names = []
counts = []

for i in top_10:
    names.append(i[0])

for i in top_10:
    counts.append(i[1])

# ok now to plot
ind = np.arange(10)
plt.bar(ind, counts)
# need to figure out how to rotate the labels 90 degrees
plt.xticks(ind+width/2., names)
plt.show()


### ADVERSE EVENTS EXPLORATION ###

# this gives us the count of the top x number of events for a drug
# there are a lot of if statements because not ever event has an openfda section
# not every openfda section has a generic_name section
def generic_name_counter(num):
    generics_count = Counter()
    for i in data_events:
        for j in i['patient']['drug']:
            if 'openfda' in j:
                if 'generic_name' in j['openfda']:
                    for k in j['openfda']['generic_name']:
                        generics_count[k] += 1
    return generics_count.most_common(num)


### DRUG RECALLS EXPLORATION ###
# let's look at all Class recall distributions
# I = most severe, II = moderately severe, III = not severe

def class_divider():
    class_one = []
    class_two = []
    class_three = []
    for i in data_events:
        if i['classification'] == 'Class I':
            class_one.append(i)
        if i['classification'] == 'Class II':
            class_two.append(i)
        if i['classification'] == 'Class III':
            class_three.append(i)


