#!/usr/bin/env python3

import requests
import json
import csv

url = "http://localhost:8000/user"
headers = {"Content-Type": "application/json"}
payload = {
    "username": "lain",
    "password": "kkf4if4g4v@ł",
    "email": "example@mail.com",
    "full_name": "fake name"
}

r = requests.post(url, data=json.dumps(payload),  headers=headers)
print(r.url)
print(r.text)
rr = r.json()

for k,v in rr.items():
    print(f"{k}: {v}")
