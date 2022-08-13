#!/usr/bin/env python3

import requests
import json

url = "http://localhost:8000/items"
payload = {"item_id": "javier", "q": "cosa"}
r = requests.get(url, params=payload)

print(r.url, r.status_code)
print(r.text)
