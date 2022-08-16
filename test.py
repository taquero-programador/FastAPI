#!/usr/bin/env python3

import requests
import json
import csv

url = "http://localhost:8000/items/545"
headers = {"Content-Type": "application/json"}
payload = {
  "name": "Foo",
  "price": 35.4,
}

r = requests.put(url, data=json.dumps(payload), headers=headers)
print(r.url)
print(r.text)
rr = r.json()

for k,v in rr.items():
    print(k,v)
