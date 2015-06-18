##### THIS FILE IS FOR DATA CLEANING #####

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
events = client.drugs.adverse_events6
enforcement = client.drugs.enforcement

### STEP 1: FLATTEN THE DATA ###
cursor_recalls = enforcement.find({})
documents_recalls = []
map(lambda x: documents_recalls.append(x['results']), cursor_recalls)
print "done with documents step: "

""" there are 100 items stored in each document so now I have to
iterate through each document and pull out the specific item.  One
document contains 100 items... """

data_recalls = []

for k in documents_recalls:
    map(lambda x: data_recalls.append(x), k)
    # for l in k:
    #     data_events.append(l)
print "done with data step: "

print len(data_recalls)

""" now we have to start to flatten out the data.  The data is
nested JSON so I'm only going to extract the parts that I need.
There are two levels of keys that I'll be extracting from...
first and second """

# test is the list of lists we are going to append to
test = []

# headers are the headers of the list of lists file
headers = ['id', '@epoch', 'classification', 'recall_initiation_date', 'report_date', 'brand_name','generic_name' 'spl_id', 'reason_for_recall']

# the list of our keys that aren't nested
first = ['@epoch', 'classification', 'recall_initiation_date', 'report_date','reason_for_recall']

# the list of the keys that are nested
second = ['brand_name','generic_name', 'spl_id']
keys = ['brand_name', 'generic_name', 'spl_id']
test.append(headers)

""" the goal is to create a list of lists. sometimes a key does
not exist...if it doesn't, then we skip that row """

documents_recalls = []



for i in data_recalls:
    if i['openfda'] != {}:
    # if all (k in j for k in keys):
        row = []
        row.append(i['@id'])
        row.extend((i[m] for m in first))
        row.extend((i['openfda'][n] for n in second))
        test.append(row)
    else:
        pass
print len(test)

""" now that we have our data flattened out into list of lists
it is time to save it to a csv file """


import csv

with open ("recalls3.csv", "wb") as f:
    writer = csv.writer(f)
    try:
        writer.writerows(test)
    except:
        print "data not good..."
print "done with csv step: "

