#!/usr/bin/env python3

from fastapi import FastAPI, Query
from typing import Union

app = FastAPI()

@app.get("/items")
async def read_items(
    q: Union[str, None] = Query(default=None, include_in_schema=False)):
    if q:
        return {"q": q}
    else:
        return {"q": "not found!"}
