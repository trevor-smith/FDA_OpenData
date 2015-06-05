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
events = client.drugs.adverse_events

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
    for i in range(14):
        tracker = i

        """ num and num_1000 are how I am going to iterate through the
        cursor by taking slices """

        num = i*1000
        num_1000 = num + 1000
        cursor_events = events.find({})[num:num_1000]
        documents_events = []
        for j in cursor_events:
            documents_events.append(j['results'])
        print "done with documents step: " + str(tracker)

        """ there are 100 items stored in each document so now I have to
        iterate through each document and pull out the specific item.  One
        document contains 100 items... """

        data_events = []
        for k in documents_events:
            for l in k:
                data_events.append(l)
        print "done with data step: " + str(tracker)

        """ now we have to start to flatten out the data.  The data is
        nested JSON so I'm only going to extract the parts that I need.
        There are two levels of keys that I'll be extracting from...
        first and second """

        # test is the list of lists we are going to append to
        test = []

        # headers are the headers of the list of lists file
        headers = ['safetyreportid', 'receivedate', 'country', 'serious', 'transmissiondate', 'actiondrug', 'medicinalproduct', 'drugcharacterization']

        # the list of our keys that aren't nested
        first = ['safetyreportid', 'receivedate', 'occurcountry', 'serious', 'transmissiondate']

        # the list of the keys that are nested
        second = ['actiondrug', 'medicinalproduct', 'drugcharacterization']
        keys = ['medicinalproduct', 'actiondrug', 'drugcharacterization']
        test.append(headers)

        """ the goal is to create a list of lists. sometimes a key does
        not exist...if it doesn't, then we skip that row """

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

        """ now that we have our data flattened out into list of lists
        it is time to save it to a csv file """

        import csv

        with open("patients"+"_"+str(tracker)+".csv", "wb") as f:
            writer = csv.writer(f)
            writer.writerows(test)
        print "done with csv step: " + str(tracker)

flatten_patients_data()
