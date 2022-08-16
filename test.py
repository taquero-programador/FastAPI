#!/usr/bin/env python3

import requests
import json
import csv

url = "http://localhost:8000/offers"
headers = {"Content-Type": "application/json"}
payload = {
  "name": "offer",
  "description": "desc offer",
  "price": 4545,
  "items": [
    {
      "name": "items",
      "description": "desc item",
      "price": 450,
      "tax": 1.16,
      "tags": [
        "dos",
        "uno",
        "tres"
      ],
      "images": [
        {
          "url": "https://google.com",
          "name": "google"
        },
        {
          "url": "https://duck.com",
          "name": "duck"
        }
      ]
    }
  ]
}


r = requests.post(url, data=json.dumps(payload), headers=headers)
print(r.url)
print(r.text)
rr = r.json()
