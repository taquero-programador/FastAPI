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

# https://fastapi.tiangolo.com/tutorial/body-multiple-params/#singular-values-in-body
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

"""
Cuerpo de la solicitud.
al enviar datos del cliente al API se envian como un body request.
la solicitud es una respuesta de datos de la API al cliente.
"""
# pydantic BaseModel. arriba de py3.10 no se requiere Union, en su lugar usar val: str | None = None
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union

class Item(BaseModel):
    name: str
    desc: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    return item

# generar una solicitud con requests
import requests
import json

url "http://localhost:8000/items/"
payload = {
    "name": "Musk",
    "desc": "Tesla",
    "price": 55555555555,
    "tax": 0.16
}
headers = {"Content-Type": "application/json"}
r = requests.post(url, data=json.dumps(payload), headers=headets)
print(r.status_code) # 200
print(r.text) # retorna el dict de la solicitud
# dentro de las funciones se puede acceder a los atributos de la clase
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    desc: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_wtax = item.price * item.tax
        ite_dict.update({"net": price_wtax})
    return item_dict

# solicitar cuerpo + parametro de ruta al mismo tiempo
# parametros de ruta deben obtenerse de la ruta y los parametros de funcion que son modelos pydantic
# se obtiene del cuerpo de la solicitud
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    desc: Union[str, None] = None
    price: float
    tax: Union[float, str] = None

app = FastAPI()

@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item_dict()}
# es PUT. el id se envia sobre la url/300 y los valores se envian sobre el body requests de put
# **item.dic() retorna los valores de body requests + el item_id en un solo dict
# para poder manipular los datos debo de hacer un casting de str a dict
import json
r_dict = r.json() # de string lo pasa a un dict json

# body requests + ruta + parametro de consulta. todo al mismo tiempo
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    desc: Union[str, None] = None
    price: float
    tex; Union[float, None] = None

app = FastAPI()

@app.put("/items/{item_id}")
async def create_item(
    item_id: int, item: Item, q: Union[str, None] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result
# id y q se envian en la url http://localhost:8000/items/100?q=qq y lo demas sobre el body requests

# parametros de consulta y validacion. FastAPI permite info adicional y validacion para sus parametros
from typing import Union
from fastapi import FastAPI

app = FastAPI()
@app.get("/items/")
async def read_items(q: Union[str, None] = None):
    result = {"items": [{"item_id": "Foo"}, {"item_id": "bar"}]}
    if q:
        result.update({"q": q})
    return result
# validación adicional. validar q evitando exceder 50 caracteres
# en este caso Query se pasa como un valor por defecto, permitiendo ser None y validar en caso de pasar un valor
from typing import Union
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items")
async def read_items(q: Union[str, None] = Query(default=None, max_length=50)):
    result = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        result.update({"q": q})
    return result
# hacer una solicitud
import requests
import json

url = "http://localhost:8000/items"
payload = {"q": "qweess"}
headers = {"Content-Type": "application/json"}
r = requests.get(url, params, headers=headers)
print(r.url) # con json retorna la url con caracteres extraños
# sin json retorna una url normal
# al pasar un valor que exceda max_length retorna un error
# añadir más vaidaciones
from typing import Union
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items")
async def rea_items(
    q: Union[str, None] = Query(default=None, min_length=3, max_length=21)):
    result = ("items": [{"item_id": "Foo"}, {"item_id": "bar"}])
    if q:
        result.update({"q": q})
    return result
# añadir condicones adicionles con regex
from typing import Union
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items")
async def read_items(q: Union[str, None] = Query(
    default=None, min_length=3, max_length=20, regex="^fixed$"
)):
    result = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        result.update({"q": q})
    return result
# la palabra debe ser fixed ^ indica como inicia y $ como termina
# valores predeterminados. dentro de Query se puede definir un valor predeterminado ademas de None
# esto puede reemplazar Union pero ya no permite mas de un tipo de dato
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items")
async def read_items(q: str = Query(default="fixedquery", min_length=3)):
    result = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        result.update({"q": q})
    return result
# hacerlo obligatorio. usar default=...
# requerido con None. usando Union
from typing import Union
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items")
async def read_items(
    q: Union[str, None] = Query(default=..., min_length=3)):
    result = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        result.update({"q": q})
    return result
# usar pydantic Required en ligar de ...
from fastapi import FastAPI
from pydantic import Required

app = FastAPI()

@app.get("/items")
async def read_items(q: str = Query(default=Required, min_length=3)):
    result = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        result.update({"q": q})
    return result
# lista de parametros de consulta/valores multiples. recibir una lista de valores
from typing import List, Union
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items")
async def read_items(q: Union[List[str]= None] = Query(default=None)):
    result = {"q": q}
    return result
# con la url se pasa http://localhost:8000/items?q=www&q=xxxx o puede ir vacio
# sin Query y usando List no permite ni uno ni varios. returna un dict con clave y una lista con varios valores

# pasar una lista como valores predeterminados
from typing import List
from fastapi import FastAPI

app = FastAPI()

@app.get("/items")
async def read_items(q: List[str] = Query(default=["foo", "bar"])):
    result = {"q": q}
    return result
# tambien se puede usar directamente list pero no se validaran los datos

# declarar más metadatos. title, description (son para los docs)
from typing import Union
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items")
async def read_items(
    q: Union[str, None] = Query(default=None, title="Query string",
    description="desc", min_length=3)):
    result = {"items": [{"item_id": "Foo"}, {"item_id": "bar"}]}
    if q:
        result.update({"q": q})
    return result
# alias. asignar un alias al parametro. ?item-query=value
from typing import Union
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items")
async def read_items(
    q: Union[str, None] = Query(default=None, alias="item-query")):
    result = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        result.update("q": q)
    return result
# la solicitud seria ?item-query=valor

# parametros obsoletos.
# cuando un parametro ya no se usa se tiene que matener para que en la documentación el cliente lo vea
# donde q en seria en Query(deprecated=True). definir dentro y al final de Query()

# excluir de OpenAPI. para excluir un parametro usar include_in_schema=False
from typing import Union
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items")
async def read_item(
    hquery: Union[str, None] = Query(default=None, include_in_schema=False)):
    if hquery:
        return {"hquery": hquery}
    else:
        return {"haquery": "not found!"}
# se puede enviar mediante la url pero en docs no va a mostrar el body

# parametros de ruta y validación de ruta
# Path permite los mismo tipos de validación y metadatos que Query
from typing import Union
from fastapi import FastAPI, Path, Query

app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(title="The ID of the item to get"),
    q: Union[str, None] = Query(default=None, alias="item-query"),):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
# falla en Path requiere un argumento. al parecer requiere default=

# ordenar los parametros a gusto propio. por defecto python devolveria error en esto a=100, b
# ya que no puede ir primero un argumento predefinido y después un no definido. usar * al inicio de todos los params
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(
    *, item_id: int = Path(title="titulo"), q: str):
    result = {"item_id": item_id}
    if q:
        result.update({"q": q})
    return result
# url http://localhost:8000/items/100?q=string


"""
gt: mayor que >
ge: moyor o igual >=
lt: menor que <
le: menor o igua =<
"""
# validacion de mayor o igual con ge
from fastapi import FastAPI, Path

app = FastAPI()


@app.get("/items/{item_id}")
async def read_items(
    *, item_id: int = Path(default=int, title="The ID of the item to get", ge=1), q: str
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
# donde ge le dice que debe ser igual o mayor a 1 /1?q=sde

# validacion de números: mayor gt > y menor o igual le <=.
from fastapi import FastAPI, Path

app = FastAPI()


@app.get("/items/{item_id}")
async def read_items(
    *,
    item_id: int = Path(default=int, title="ID item", gt=0, le=1000),
    q: str):
    result = {"item_id": item_id}
    if q:
        result.update({"q": q})
    return result
