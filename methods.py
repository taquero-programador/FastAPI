#!/usr/bin/env python3

import requests
import json
import csv
import os

url = "http://localhost:8000/items/{}"
headers = {"Content-Type": "application/json"}
data = {
    1: {"name": "Python",
    "description": "desc test",
    "price": 5451,
    "tax": 10.5,
    "tags": ["uno", "dos", "tres"]},
    2: {
        "name": "Rust",
        "description": None,
        "price": None,
        "tax": 1.16,
        "tags": ["u2", "cure"]},
    3: {
        "name": None,
        "description": "prueba",
        "price": None,
        "tax": 45.52,
        "tags": []
    }
}

def update_payload():
    payload = {}
    {print(k,v["name"]) for k,v in data.items()}
    select_id = input("Select N# value: ")
    for k,v in data.items():
        if k == int(select_id):
            payload.update(v)
    return payload


def iter_items(**kwargs):
    for k, v in kwargs.items():
        print(f"{k}: {v}")


def get():
    id_item = input("id: ")
    url_ = url.format(id_item)
    r = requests.get(url_, headers=headers)
    rr = r.json()
    os.system("clear")

    print(f"url:{r.url} status:{r.status_code}")
    iter_items(**rr)


def post():
    id_item = input("id: ")
    url_ = url.format(id_item)
    r = requests.post(url_, data=json.dumps(update_payload()), headers=headers)
    rr = r.json()
    os.system("clear")
    print(f"url:{r.url} status:{r.status_code}")
    iter_items(**rr)


def put():
    id_item = input("id: ")
    url_ = url.format(id_item)
    r = requests.put(url_, data=json.dumps(update_payload()), headers=headers)
    rr = r.json()
    os.system("clear")

    print(f"url:{r.url} status:{r.status_code}")
    iter_items(**rr)


def patch():
    id_item = input("id: ")
    url_ = url.format(id_item)
    r = requests.patch(url_, data=json.dumps(update_payload()), headers=headers)
    rr = r.json()
    os.system("clear")

    print(f"url:{r.url} status:{r.status_code}")
    iter_items(**rr)

def delete():
    pass
