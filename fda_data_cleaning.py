##### THIS FILE IS FOR DATA CLEANING #####

### IMPORTS ###
from pymongo import MongoClient
import pandas as pd
import numpy as np
import pprint

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


