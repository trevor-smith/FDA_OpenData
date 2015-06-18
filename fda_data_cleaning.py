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

""" the data is nested JSON and I'd like to get it tabular so I'm going
to flatten it with the function I've created below.  This one is extracting
the data related to the patient and the drugs they have in their system. """

def flatten_patients_data():

    """ this function reads in the data from mongodb in chunks because
    the size of the data is too large to fit into memory.  I read in each
    iteration and then extract the data I need and save to csv"""

    """ this is how we are going to iterate through the mongodb cursor """

    print "here we go............."
    for i in range(0,30):
        tracker = i

        """ num and num_500 are how I am going to iterate through the
        cursor by taking slices """

        num = i*500
        num_500 = num + 500
        cursor_events = events.find({})[num:num_500]
        documents_events = []
        map(lambda x: documents_events.append(x['results']), cursor_events)
        # for j in cursor_events:
        #     documents_events.append(j['results'])
        print "done with documents step: " + str(tracker)

        """ there are 100 items stored in each document so now I have to
        iterate through each document and pull out the specific item.  One
        document contains 100 items... """

        data_events = []

        for k in documents_events:
            map(lambda x: data_events.append(x), k)
            # for l in k:
            #     data_events.append(l)
        print "done with data step: " + str(tracker)

        print len(data_events)

        """ now we have to start to flatten out the data.  The data is
        nested JSON so I'm only going to extract the parts that I need.
        There are two levels of keys that I'll be extracting from...
        first and second """

        # test is the list of lists we are going to append to
        test = []

        # headers are the headers of the list of lists file
        headers = ['safetyreportid', '@epoch', 'receivedate', 'serious', 'transmissiondate', 'medicinalproduct', 'drugcharacterization']

        # the list of our keys that aren't nested
        first = ['@epoch', 'receivedate', 'serious', 'transmissiondate']

        # the list of the keys that are nested
        second = ['medicinalproduct', 'drugcharacterization']
        keys = ['medicinalproduct', 'drugcharacterization']
        test.append(headers)

        """ the goal is to create a list of lists. sometimes a key does
        not exist...if it doesn't, then we skip that row """

        documents_events = []



        for i in data_events:
            for j in i['patient']['drug']:
                if all (k in j for k in keys):
                    row = []
                    row.append(i['safetyreportid'])
                    row.extend((i[m] for m in first))
                    row.extend((j[n] for n in second))
                    test.append(row)
                else:
                    pass
        print len(test)

        """ now that we have our data flattened out into list of lists
        it is time to save it to a csv file """

        data_events = []

        import csv

        with open ("patientsv3"+"_"+str(tracker)+".csv", "wb") as f:
            writer = csv.writer(f)
            try:
                writer.writerows(test)
            except:
                print "data not good..."
        print "done with csv step: " + str(tracker)

flatten_patients_data()
