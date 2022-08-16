#!/usr/bin/env python3

import requests
import json
import csv

url = "http://localhost:8000/items/444"
headers = {"Content-Type": "application/json"}
payload = {
  "item": {
    "name": "john",
    "description": "vocals",
    "price": 5555,
    "tax": 1.15
  },
  "user": {
    "username": "jdevil",
    "full_name": "jonathan davis"
  },
    "importance": 25
}

r = requests.put(url, data=json.dumps(payload), headers=headers)
print(r.url)
print(r.text)
rr = r.json()
