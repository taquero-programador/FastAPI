#!/usr/bin/env python3

import requests
import json
import csv

url = "http://localhost:8000/index-weights"
headers = {"Content-Type": "application/json"}
payload = {
    1: 1.75,
    2: 3.85
}

r = requests.post(url, data=json.dumps(payload), headers=headers)
print(r.url)
print(r.text)
rr = r.json()

for k,v in rr.items():
    print(k,v)
