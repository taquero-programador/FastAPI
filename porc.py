#!/usr/bin/env python3

import requests
import json
from methods import url, get, put, post, patch

url = "http://localhost:8000/{}/{}"
res = True
while res:
    if res == "1":
        get()
    elif res == "2":
        post()
    elif res == "3":
        put()
    elif res == "4":
        patch()
    elif res == "5":
        pass
    print("""select metod
    [1] GET
    [2] POST
    [3] PUT
    [4] PATCH
    [5] DELETE""")
    res = input("Method?: ")
