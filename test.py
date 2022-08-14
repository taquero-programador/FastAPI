#!/usr/bin/env python3

import requests
import json

url = "http://localhost:8000/items/"
payload = {
  "name": "bender",
  "desc": "dev",
  "price": 5000,
  "tax": 0.16
}
headers = {"Content-Type": "application/json"}
r = requests.post(url, data=json.dumps(payload))

print(r.url)
print(r.text)
