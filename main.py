#!/usr/bin/env python3

from fastapi import FastAPI

app = FastAPI()

#@app.get('/')
#async def root():
#    return {'mensaje': 'hello world!!'}

# usar el metodo string format
#@app.get('/items/{item_id}')
#async def read_item(item_id):
#	return {'item_id': item_id}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}