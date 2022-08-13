#!/usr/bin/env python3

from fastapi import FastAPI
from typing import Union
app = FastAPI()

@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: Union[str, None] = None):
    item = {"item_id": item_id}
    if needy:
        item.update({"needy": needy})
    return item
