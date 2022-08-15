#!/usr/bin/env python3

import requests
import json
import csv

url = "http://localhost:8000/items"
headers = {"Content-Type": "application/json"}
payload = {"item-query": "qwertyuiopasdfgh"}
r = requests.get(url, params=payload, headers=headers)
print(r.url)
print(r.text)
rr = r.json()
for k,v in rr.items():
    print(k,v)
