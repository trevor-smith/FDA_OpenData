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
for i in cursor_labels:
    documents_labels.append(i['results'])

documents_events = []
for i in cursor_events:
    documents_events.append(i['results'])

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

### FLATTENING DATA ###
# data already exists in list called 'data_events'

print len(data_events)
# this is 223,200

test = []
headers = ['safetyreportid', 'receivedate', 'country', 'serious', 'transmissiondate', 'actiondrug', 'medicinalproduct', 'drugcharacterization']
# the list of our keys that aren't nested
first = ['safetyreportid', 'receivedate', 'occurcountry', 'serious', 'transmissiondate']
# the list of the keys that are nested
second = ['actiondrug', 'medicinalproduct', 'drugcharacterization']
keys = ['medicinalproduct', 'actiondrug', 'drugcharacterization']
test.append(headers)

# the goal is to create a list of lists
# sometimes a key does not exist...if it doesn't, then we skip that row
for i in data_events:
    for j in i['patient']['drug']:
        if all (k in j for k in keys):
            row = []
            # this loop appends the items that are not as far nested
            # that's why it refers to i
            for m in first:
                row.append(i[m])
            # this loop appends the items that are more nested
            # that's why it refers to j
            for n in second:
                row.append(j[n])
            test.append(row)
        else:
            pass

print len(test)
# now it has been expanded to 351,097

### SAVING TO CSV ###
# we want to save this file as a csv
# we can then store it in sql OR just read it right into a pandas DF

import csv

with open("patients.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(test)

