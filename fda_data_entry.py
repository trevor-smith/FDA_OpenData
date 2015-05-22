# the goal of this is to just run different queries to the FDA API
# access: https://open.fda.gov/api

# IMPORTS
import requests
import json
import cnfg
import pprint
from pymongo import MongoClient
import time

# already have some data in the db, now just querying it
client = MongoClient()
labels = client.drugs.drug_labeling


for i in range(0,1000):
    j = int(i*100)
    response = requests.get("https://api.fda.gov/drug/label.json?api_key=GETYOUROWNAPIKEY&search=&limit=100&skip=" + str(j) + "\"")
    labels.insert(response.json())
    # loop to not run over the 240 requests per minute threshold
    if i % 240 == 0:
        time.sleep(30)
        print "finished iteration: " + str(i)

# labels.remove( {'error': {u'message': u'Invalid skip parameter value.', u'code': u'BAD_REQUEST'}} )
# labels.remove( {'error': {u'message': u'No matches found!', u'code': u'NOT_FOUND'}} )
