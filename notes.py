# FastAPI

# crear un entorno virtual para fastapi
python3 -m venv 'name'
source 'name'/bin/activate
pip3 install --uprade pip3
pip3 -m install fastapi pydantic
pip3 install uvicorn[standard]

# primeros pasas. Archivo simple

from fastapi import FastAPI

app = FastAPI() # instancia para fastapi

@app.get("/")
asycn def root():
    return {"mensaje"}

# ejecutar uvicorn main:app --reload. donde main es el nombre de la app, app es el nombbre de la instancia dentro del modulo .pu (tambien es parte del decorador)
# y --reloads recarga despues de cada cambio
# localhost:8000 debe retorna el mensaje pues es la ruta raiz
# en localhost:8000/docs permite visualizar e interactuar con los recursos de la api
# localhost:/8000/redoc herramienta opensource para generar documentación
# puede devolver un dict o list con str e int, inlcuido una gran variedad de moelos que se convertirar a JSON

# paramatros de ruta. se pueden declarar como parametros o variables que luego se pasaran como tipos str
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}

# en localhost:8000/items/cosa rebe retornar un dict
# definir el tipo de valor a recibir usando anotaciones de tipo

from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
# retorna error si se pasa algo que no sea int y permite comatibilidad a su destino
# pydantic que encarga de realizar la validación
"""
El orden import.
suponiendo que se tiene /users/me para obtener los datos del usuario actual
y tambien /users/{user_id} para obtener los datos de un usuario especifico.
por lo que /me debe estar antes de /{user_id}
"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "usuario actual"}

@app.get("/users/{user_id}")
async def read_user(user_id):
    return {"user_id": user_id}

"""
valores predefinidos
operaciones que reciben un parametro de ruta pero se desea que los parametros
de ruta estren predefinidos
"""
# crear una enumeracion con Enum. al pasar str la api sabra que son string
from enum import Enum
from fastapi import FastAPI

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()

@app.get("model/{model_name}")
async def get_model(model_name):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "mensaje": "Deep learning"}

    if model_name == ModelName.resnet:
        return {"model_name": model_name, "mensaje": "LeCNN"}

    return {"model_name": model_name, "mensaje": "Debian BTW..."}

"""
parametros de ruta que contienen rutas
supongamos que se tiene una endpoint /files/{file_path}
pero se necesita una ruta paht como /home/user/file.csv.

entonces el endpoint deberia ser algo como /files/home/user/file.csv

usar una opcion de starlette /files/{file_paht:path}
dode file_path es el parametro y :path  le dice que debe conicidir con cualquier ruta
"""
from fastapi import FastAPI

app = FastAPI()

@app.get("/files/{file_paht:path}")
async def read_files(file_path: str):
    return {"file_path": file_path}
# al copiar la ruta puede junto a la url puede tener doble //, en amos casos funciona
# y retorna un string de la ruta del archivo

# parametros de consulta. cuando se declaran parametros que no son parte de la ruta
# se interpretan como parametros de consulta
from fastapi import FastAPI

app = FastAPI()

fake_items = [{"item_name": "Foo"},
              {"item_name": "Bar"},
              {"item_name": "Baz"}]

@app.get("/items")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items[skip : skip + limit]
# esto vendria a ser un conjunto de pares clave:valor que van depués de ?
# ejemlo
localhost:/items/?skip=0&limit=10
# skip con un valor de 0 y limit con 10

# parametros opcionales. declarar parametros de consulta opcional, configurando su valor como None
from typing import Union
# Union permite asignar varios tipos de valor a un elemento
from fastapi import FastAPI

app = FastAPI()

@app.get("/ite,s/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
# donde q sera opcional y por defecto sera None
# para pasar dos valores es /items/item_name?q=valor_de_q
# uno solo seria /items/item_name

# conversion de tipo de parametro en consulta. declarra bool
from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def get_item(item_id: str, q: Union[str, Union] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
            item.update(
                {"descripcion": "desc"}
            )
    return item
# la url completa seria http://localhost:8000/items/uno?q=dos&short=false

# multiples rutas y parametros de consulta. no se declaran en orden especifico
from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}/items/{item_id}")
async = def read_user_item(
    user_id: str, item_id: str, q: Union[str, None] = None, short: bool=false):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "desc"})
    return item
# http://localhost:8000/users/javier/items/coca?q=get&short=false

# parametros de consulta requeridos
# pasar None si no sea desea establecer un valor predeterminado
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_user_id(item_id: str, needy: str = None):
    item = {"item_id": item_id}
    if needy:
        item.update({"needy": needy})
    return item
# valores predeterminados y opcionales

