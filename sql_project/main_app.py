#!/usr/bin/env python3

import requests
import json
import os

url = "http://localhost:8000/users/"
urli = "http://localhost:8000/items/?{}&{}"
headers = {"Content-Type: application/json"}


def iter_data(*args, **kwargs):
    if kwargs:
        print(kwargs)

    if args:
        for i in args:
            print(i)


def get_url(id_user=None):
    if id_user:
        return iter_data(**requests.get(url+str(id_user)).json())
    return iter_data(*requests.get(url).json())


def get_user():
    os.system("clear")
    id_user = input("id_user: ")
    return get_url(id_user)


def get_users():
    os.system("clear")
    return get_url()


def create_user():
    os.system("clear")
    print("Create User", '\n', "---------------------")
    email = input("Email: ")
    password = input("Password: " )
    payload = {"email": email, "password": password}
    return iter_data(**requests.post(url, data=json.dumps(payload)).json())


def create_item():
    os.system("clear")
    print("Create Item", '\n',  "------------------------")
    id_user = input("id_user: ")
    title = input("Title: ")
    desc = input("Description: ")
    article = {"title": title, "Description": desc}
    return iter_data(
        **requests.post(url +f"{id_user}/items/", data=json.dumps(article)).json())


def get_all_items(skip=0, limit=100):
    limit = input("Limit: ")
    os.system("clear")
    url_ = urli.format(skip, limit)
    return iter_data(*requests.get(url_).json())

crud = True
while crud:
    if crud == "1":
        create_user()
    elif crud == "2":
        create_item()
    elif crud == "3":
        get_user()
    elif crud == "4":
        get_users()
    elif crud == "5":
        get_all_items()
    elif crud == "q":
        break
    print("""Menu:
    [1] Create user
    [2] Create item for user
    [3] Get user for ID
    [4] Get all users
    [5] Get all items
    [6] Exit""")
    crud = input("Select option: ")
