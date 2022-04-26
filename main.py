#!/usr/bin/env python3

from fastapi import FastAPI
from enum import Enum


app = FastAPI()

#@app.get('/')
#async def root():
#    return {'mensaje': 'hello world!!'}

# usar el metodo string format
#@app.get('/items/{item_id}')
#async def read_item(item_id):
#	return {'item_id': item_id}

#@app.get("/items/{item_id}")
#async def read_item(item_id: int):
#    return {"item_id": item_id}

#@app.get('/users/me')
#async def read_user_me():
#    return {'user_id': 'actual user'}

#@app.get('/users/{user_id}')
#async def read_user(user_id: str):
#    return {'user_id': user_id}

class ModelName(str, Enum):

    alexnet = 'alexnet'
    resnet = 'resnet'
    lenet = 'lenet'

@app.get('/models/{model_name}')
async def get_model(model_name: ModelName):

    if model_name == ModelName.alexnet:
        return {'model_name': model_name, 'message': 'Deep learning FTW!'}

    if model_name.value == 'lenet':
        return {'model_name': model_name, 'message': 'LeCNN'}


    return {'model_name': model_name, 'message': 'residuals'}

# noprod
# app.get('/files/{files_path:path}')
# async def read_file(file_path: str):
#     return {'file_path': file_path}