#!/usr/bin/env python3

import requests
import json
import csv
from datetime import datetime
a = datetime.today()

url = "http://localhost:8000/items/458"
headers = {"Content-Type": "application/json"}
payload = {
    "title": "test",
    "timestamp": a,
    "description": "test desc"
}

r = requests.put(url, data=json.dumps(payload),  headers=headers)
print(r.url)
print(r.text)
rr = r.json()

for k,v in rr.items():
    print(f"{k}: {v}")
