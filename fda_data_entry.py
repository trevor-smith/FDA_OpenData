# the goal of this is to just run different queries to the FDA API
# access: https://open.fda.gov/api

# IMPORTS
import requests
import json
import cnfg
import pprint
from pymongo import MongoClient
import time

### EXTRACTING DRUG LABELS DATA ###
# there's around 70k drug labels
client = MongoClient()
labels = client.drugs.drug_labeling


for i in range(0,50):
    j = int(i*100)
    if i % 240 == 0:
        time.sleep(30)
    print "on iteration: " + str(i)
    response = requests.get("https://api.fda.gov/drug/label.json?api_key=h84pEssgNdT4A19c3CiHp1cKK3Gh3Aajc6GNtIq9&search=effective_time:[20150101+TO+20150331]&limit=100&skip=" + str(j) + "\"")
    labels.insert(response.json())
# loop to not run over the 240 requests per minute threshold

# cleaning up the bad data in mongodb
# labels.remove( {'error': {u'message': u'Invalid skip parameter value.', u'code': u'BAD_REQUEST'}} )
# labels.remove( {'error': {u'message': u'No matches found!', u'code': u'NOT_FOUND'}} )

## EXTRACTING RECALLS DATA ###
# there's around 4,000 events

client = MongoClient()
enforcement = client.drugs.enforcement2

print "starting the enforecement extraction..."
for i in range(0,39):
    j = int(i*100)
    response = requests.get("https://api.fda.gov/drug/enforcement.json?api_key=h84pEssgNdT4A19c3CiHp1cKK3Gh3Aajc6GNtIq9&search=&limit=100&skip=" + str(j) + "\"")
    enforcement.insert(response.json())
    print "finished iteration: " + str(i)
print "all done!"
# enforcement.remove( {'error': {u'message': u'No matches found!', u'code': u'NOT_FOUND'}} )
# enforcement.remove( {'error': {u'message': u'Invalid skip parameter value.', u'code': u'BAD_REQUEST'}} )

### EXTRACTING ADVERSE EVENTS DATA ###
# there's over 4mm events from 2004

client = MongoClient()
events = client.drugs.adverse_events6

print "starting the adverse events extraction..."

years1 = ['2008', '2009', '2010', '2011']
years2 = ['2012', '2013', '2014']
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

starts = ['01', '15']
ends = ['14', '31', '14', '28','14','31','14','30','14','31','14','30','14','31','14','31','14','30','14','31','14','30','14','31']

loops = 0
for year in years1:
    print "starting year " + str(year)
    count = 0
    for month in months:
        print "starting month " + str(month)
        for ind, start in enumerate(starts):
            for i in range(0,51):
                j = int(i*100)
                if loops % 240 == 0:
                    print "done with: " + str(loops)
                    time.sleep(59)
                try:
                    response = requests.get("https://api.fda.gov/drug/event.json?api_key=h84pEssgNdT4A19c3CiHp1cKK3Gh3Aajc6GNtIq9&search=receivedate:["+year+month+start+'+TO+'+year+month+ends[count]+"]&limit=100&skip=" + str(j) + "\"")
                    events.insert(response.json())
                except:
                    print "json not good on: "+year+month+start+'TO'+year+month+ends[count]
                loops +=1
            count +=1



loops = 0
for year in years2:
    print "starting year " + str(year)
    count = 0
    for month in months:
        print "starting month " + str(month)
        for ind, start in enumerate(starts):
            for i in range(0,51):
                j = int(i*100)
                if loops % 240 == 0:
                    print "done with: " + str(loops)
                    time.sleep(59)
                try:
                    print "https://api.fda.gov/drug/event.json?api_key=h84pEssgNdT4A19c3CiHp1cKK3Gh3Aajc6GNtIq9&search=receivedate:["+year+month+start+'+TO+'+year+month+ends[count]+"]&limit=100&skip=" + str(j) + "\""
                #     response = requests.get("https://api.fda.gov/drug/event.json?api_key=h84pEssgNdT4A19c3CiHp1cKK3Gh3Aajc6GNtIq9&search=receivedate:["+year+month+start+'+TO+'+year+month+ends[count]+"]&limit=100&skip=" + str(j) + "\"")
                #     events.insert(response.json())
                except:
                    print "json not good on: "+year+month+start+'TO'+year+month+ends[count]
                loops +=1
            count +=1
