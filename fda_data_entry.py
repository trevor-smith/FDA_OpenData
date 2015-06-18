# the goal of this is to just run different queries to the FDA API
# access: https://open.fda.gov/api

# IMPORTS
import requests
import json
import cnfg
import pprint
from pymongo import MongoClient
import time

# ### EXTRACTING DRUG LABELS DATA ###
# # there's around 70k drug labels
# client = MongoClient()
# labels = client.drugs.drug_labeling


# for i in range(0,1000):
#     j = int(i*100)
#     if i % 240 == 0:
#         time.sleep(30)
#         print "on iteration: " + str(i)
#     response = requests.get("https://api.fda.gov/drug/label.json?api_key=h84pEssgNdT4A19c3CiHp1cKK3Gh3Aajc6GNtIq9&search=&limit=100&skip=" + str(i) + "\"")
#     labels.insert(response.json())
#     loop to not run over the 240 requests per minute threshold

# cleaning up the bad data in mongodb
# labels.remove( {'error': {u'message': u'Invalid skip parameter value.', u'code': u'BAD_REQUEST'}} )
# labels.remove( {'error': {u'message': u'No matches found!', u'code': u'NOT_FOUND'}} )

### EXTRACTING ADVERSE EVENTS DATA ###
# there's over 4mm events from 2004

client = MongoClient()
events = client.drugs.adverse_events4

print "starting the adverse events extraction..."
for i in range(6500):
    j = int(i*100)
    if i % 240 == 0:
        time.sleep(50)
        print "on iteration: " + str(i)
    try:
        response = requests.get("https://api.fda.gov/drug/event.json?api_key=h84pEssgNdT4A19c3CiHp1cKK3Gh3Aajc6GNtIq9&search=receivedate:[20080101+TO+20100101]&limit=100&skip=" + str(i) + "\"")
        # response = requests.get("https://api.fda.gov/drug/event.json?api_key=h84pEssgNdT4A19c3CiHp1cKK3Gh3Aajc6GNtIq9&search=&limit=100&skip=" + str(i) + "\"")
        map(lambda x: events.insert(x), response.json()['results'])

    except:
        print "json not good"


## EXTRACTING RECALLS DATA ###
# there's around 4,000 events

# client = MongoClient()
# enforcement = client.drugs.enforcement

# print "starting the enforecement extraction..."
# for i in range(0,38):
#     j = int(i*100)
#     response = requests.get("https://api.fda.gov/drug/enforcement.json?api_key=h84pEssgNdT4A19c3CiHp1cKK3Gh3Aajc6GNtIq9&search=&limit=100&skip=" + str(i) + "\"")
#     enforcement.insert(response.json())
#     print "finished iteration: " + str(i)
# print "all done!"

