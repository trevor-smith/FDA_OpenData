# the goal of this is to just run different queries to the FDA API
# access: https://open.fda.gov/api

# IMPORTS
import requests
import json
import cnfg
import pprint
from pymongo import MongoClient

# already have some data in the db, now just querying it
# response = requests.get("https://api.fda.gov/drug/event.json?api_key=h84pEssgNdT4A19c3CiHp1cKK3Gh3Aajc6GNtIq9&search=&limit=99")

client = MongoClient()
adverse_events = client.drugs.adverse_events
data = adverse_events.find({})

for i in data[:2]:
    pprint.pprint(i)


