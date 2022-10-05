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
# hacerlo obligatorio. usar de fault=...
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

# body - multiples respuestas. declarar None en clases de la solicitud
from typing import Union
from fastapi import FastAPI, Path
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int = Path(default=int, title="The ID of the item to get", ge=0, le=1000),
    q: Union[str, None] = None,
    item: Union[Item, None] = None):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results
# en la funcion le dice a item que sera igua a la clase Item pero tambien puede ser None
# requests http://localhost:8000/items/0?q=qw, lo demas se envia en el body
# retorna un diccionario anidado
# mandando la peticion con requests
import requests
import json

url = "http://localhost:8000/items/545"
headers = {"Content-Type application/json"}
payload {
    "name": "jdavi",
    "description": "vocal",
    "price": 456,
    "tax": 1.75
}
r = requests.put(url, data=payload, headers=headers)
print(r.url)
print(r.text)

# declarar varios parametros de cuerpo
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

class User(BaseModel):
    username: str
    full_name: Union[str, None] = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results
# http://localhost:8000/items/123 y lo demas sobre el body
# para enviar 2 body es asi
import requests
import json

url = "http://localhost:8000/items/457"
headers = {"Content-Type": "application/json"}
payload = {
  "item": {
    "name": "john",
    "description": "vocals",
    "price": 5555,
    "tax": 1.15
  },
  "user": {
    "username": "jdevil",
    "full_name": "jonathan davis"
  }
}
r= requests.put(url, data=json.dums(payload), headers)
print(r.status_code)
print(r.url)
rr = r.json()
print(rr)
# fastapi hara la conversion para asignar cada valor item y user

# valores singulares en el cuerpo. al igual que Query y Path en body se pueden añadir parametros adicionales
# añadir importance como si fuera un body requests. se envia en body y no sobre la url
from typing import Union
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

class User(BaseModel):
    username: str
    full_name: Union[str, None] = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User, importance: int = Body(...)):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results
# usar (...) para obligatorio pero no marca error si se envia vació.
# se puede pasar un valor por defecto. permite gt, ge, lt y le
# espera algo como esto
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    },
    "importance": 5
}

# incrustrar un solo parametro en el body.
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(embed=True)):
    results = {"item_id": item_id, "item": item}
    return results
# en este caso a pesar de ser solo un body lo espera como un dict {item: {k:v }} en lugar de {k:v}

# body - campos. declarar parametros y validacion en modelos Pydantic con Field
from typing import Union
from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: Union[float, None] = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(..., embed=True)):
    results = {"item_id": item_id, "item": item}
    return results

# body - modelos anidados.
# campos de lista. usar list = [] directamente de python
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: list = []


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
# tags permite varios valores pasados dentro de una lista

# en versiones superiores py3.9 se puede usar list para las declaraciones de tipo, en versiones menores
# from typing import List
from typing import List, Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: List[str] = []


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
# vendria a ser lo mismo que tags: Union[str, None] = None
# >=py3.9 lista: list[str], <=py3.9 lista: List[str] importando List de typing

# establecer tipos. supongamos que se pasa una lista pero deseamos que los valores sea unicos. usar set()
from typing import Set, Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results

# modelos anidados. similar a la herencia, utiliza el objeto de una clase para ser usada en otra y cambiar los parametros
from typing import Set, Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Image(BaseModel):
    url: str
    name: str


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()
    image: Union[Image, None] = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
# la clase Item crea atributo que puede ser vacio o usar el atributo de la clase Imagen
# espera algo como esto
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": ["rock", "metal", "bar"],
    "image": {
        "url": "http://example.com/baz.jpg",
        "name": "The Foo live"
    }
}
# tipos especiales y validación. además de lso tipos str, int, float, se puede usar algo más avanazado para str
# en lugar de str usar HttpUrl
from typing import Set, Union
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()
    image: Union[Image, None] = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
# con HttpUrl valida la cadena en busca de una url valida requiere http

# atributos con lista de submodelos List, Set, etc.
from typing import List, Set, Union
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()
    images: Union[List[Image], None] = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
# donde Item de nuevo crea un atributo que puede ser vacio o pasarte una lista con diccionarios
# espera algo como
{
    "name": "zidane",
    "description": "desc",
    "price": 5425,
    "tax": 0,
    "tags": ["rock", "punk"],
    "image": [
        {
        "url": "https://google.com",
        "name": "goimg"},
        {
            "url": "https://reddit.com",
            "name": "reddit"
        }
    ]
}

# modelos profundamente anidados.
from typing import List, Set, Union
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()
    images: Union[List[Image], None] = None


class Offer(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    items: List[Item]


@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer
# offer herada todos los atributos desde Item
# y espera algo como esto y el orden va de Offer, Item e Image
# el primer body se envia solo k,v y los siguientes como una lista de diccionarios.
# se debe a que al heredar el atributo se pasa como items: List[Item]
# si no se especifica se pasa como una clave y su valor un diccionario
{
  "name": "offer",
  "description": "desc offer",
  "price": 4545,
  "items": [
    {
      "name": "items",
      "description": "desc item",
      "price": 450,
      "tax": 1.16,
      "tags": ["dos","uno","tres"],
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
# cuerpo de listas puras. puede usarse list directo de py>=3.9
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()


class Image(BaseModel):
    url: HttpUrl
    name: str

@app.post("/images/multiple/")
async def create_multiple_images(images: List[Image]):
    return images

# dict. declarar un clave de un tipo de un valor de otro. seria util cuando no se sabe el valor de laas claves
# o recibir una una clave de tipo int y valores como float
from typing import Dict
from fastapi import FastAPI

app = FastAPI()


@app.post("/index-weights/")
async def create_index_weights(weights: Dict[int, float]):
    return weights
# es diccionario se envia como un body. si en el decorador no se solicita una un argumento, el valor se envia como body
{
    1: 5.78,
    2: .65
}

# declarar solicitud de datos de ejemplo. Pydantic schema_extra
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
# se añade un body a schema_extra para que se usada por defecto y visible en la documentación.
# usar **item.dict() para devolver un solo dict
# en la docs se muestra pedo igual se tiene que mandar el body

# Field argumentos adicionales. con Field() se puede añadir informacion adicional para esquema
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str = Field(example="Foo")
    description: Union[str, None] = Field(default=None, example="A very nice Item")
    price: float = Field(example=35.4)
    tax: Union[float, None] = Field(default=None, example=3.2)


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
# similar a schema_extra. en el esquema se muestra el valor por defecto en docs
# al enviar la peticion se puede omitir pero no regresa los example. no añade ninguna validación

# example y examples. body con example
from typing import Union
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item = Body(...,
        example={
            "name": "Foo",
            "description": "A very nice Item",
            "price": 35.4,
            "tax": 3.2,
        },
    ),
):
    results = {"item_id": item_id, "item": item}
    return results
# body permite multiples examples como un dict.
from typing import Union
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Item = Body(
        examples={
            "normal": {
                "summary": "A normal example",
                "description": "A **normal** item works correctly.",
                "value": {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
            },
            "converted": {
                "summary": "An example with converted data",
                "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                "value": {
                    "name": "Bar",
                    "price": "35.4",
                },
            },
            "invalid": {
                "summary": "Invalid data is rejected with an error",
                "value": {
                    "name": "Baz",
                    "price": "thirty five point four",
                },
            },
        },
    ),
):
    results = {"item_id": item_id, "item": item}
    return results
"""
en dos mostrara 3 tipos de examples
a normal example: muestra los valores por defecto y como deberian ir
example converte: muesta como haria la conversion
invalid data: muestra los datos que no se deben ingresar y la conversion que
no puede hacer
"""

"""
tipos de datos adicionales. datos adicionales que se pueden usar
UUID: identificado universal unico, ID usado por base de datos y OS str.
datetime.datetime: solicitud y respuesta en str ISO 8601 2008-09-15T15:53:00+05:00.
datetime.date: 2008-09-15 str
datetime.time: 14:23:55.003 str
datetime.timedelta: float
frozenset: st
- solicitud: se lee un listado, elimina duplicados y convierte a un set()
- respuesta set a list
bytes: solicitud y respuesta str
Decimal: solicitu y respuesta str
"""
from datetime import datetime, time, timedelta
from typing import Union
from uuid import UUID
from fastapi import Body, FastAPI

app = FastAPI()


@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: Union[datetime, None] = Body(default=None),
    end_datetime: Union[datetime, None] = Body(default=None),
    repeat_at: Union[time, None] = Body(default=None),
    process_after: Union[timedelta, None] = Body(default=None),
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
    }
# el uuid se envia en la url y lo demas en un body. RECAP

# parametros de cookies.
from typing import Union
from fastapi import Cookie, FastAPI

app = FastAPI()


@app.get("/items/")
async def read_items(ads_id: Union[str, None] = Cookie(default=None)):
    return {"ads_id": ads_id}

# parametros de headers.
from typing import Union
from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(user_agent: Union[str, None] = Header(default=None)):
    return {"User-Agent": user_agent}
# el header se envia sobre en el body sobrel el requests

# conversion automatica. python no permite el guin medio. habilitar o deshabilitar con True or False
from typing import Union
from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(
    strange_header: Union[str, None] = Header(default=None, convert_underscores=False)
):
    return {"strange_header": strange_header}

# encabezados duplicados. encabezados con mutiples valores
# X-Token puede recibir una lista con varios valores
from typing import List, Union
from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(x_token: Union[List[str], None] = Header(default=None)):
    return {"X-Token values": x_token}

# modelos de respuesta. response_model puede ser usado en cualquier operacion de rutas
from typing import List, Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: List[str] = []


@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item
"""
response_model es parte del decorado y no de la funcion.
FastAPI usa response_model para
- convertir los datos de salida a su declaración de tipo
- validar datos
- agrega schema json en a respuesta de la ruta
- sera usado en la documentación
"""
# devolver los mismos datos de entrada.
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Union[str, None] = None


# Don't do this in production!
@app.post("/user/", response_model=UserIn)
async def create_user(user: UserIn):
    return user
# con esto, lo mismo que se envia es lo mismo que se recibe
# no deberia se un problema porque el mismo usuario es quien envia la contraseña
# no almacenar ni enviar la contraseña en un requests

# agregar un modelos de salida. definir un modelo para la entrada y otro para la salida de la contraseña
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Union[str, None] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None


@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn):
    return user
"""
se recibe un modelo en UserIn, mientras que UserOut tomas los mismo valores pero sin la contraseña
el lugar de devolver todo response_model se encarga de envier el modelo modificado en lugar del original
"""

# parametros de codificacion del modelo de respuesta. usar response_model_exclude_unset=True
from typing import List, Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: float = 10.5
    tags: List[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]
# en este caso cada ID tiene un valor determinado.


# response_mode_include y response_mode_exclude. toman un set str con el nombre del atributo a incluir o excluir.
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: float = 10.5


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}


@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include={"name", "description"},
)
async def read_item_name(item_id: str):
    return items[item_id]


@app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
async def read_item_public_data(item_id: str):
    return items[item_id]
# en el caso anterior cada endpoint excluye o incluye determinados valores

# usar listas en lugar de sets
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: float = 10.5


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}


@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include=["name", "description"],
)
async def read_item_name(item_id: str):
    return items[item_id]


@app.get("/items/{item_id}/public", response_model=Item, response_model_exclude=["tax"])
async def read_item_public_data(item_id: str):
    return items[item_id]

"""
modelos adicionales.
modelos de usuarios
- el modelo de entrada debe tener una contraseña
- el modelo de salida no debe tener una contraseña
- el modelo base debe tener una contraseña cifrada.

convertir la contraseña en un hash
"""
# multiples modelos.
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Union[str, None] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None


class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: Union[str, None] = None


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved
# se crean varios modelos así como funciones para porcesar, los datos de entrada, hash de contraseña y datos de salida
# primero llamada al decorador, luego a hashes y por ultimo a DB

# reducir la duplicación. utilizas UserInDB como modelo base y crear varias sub clases
# response_model permite usar Union para pasar varios parametros que funciona como un or
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type = "car"


class PlaneItem(BaseItem):
    type = "plane"
    size: int


items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}


@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    return items[item_id]

# listado de modelos. declarar respuestas de lista de objetos
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str


items = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
]


@app.get("/items/", response_model=List[Item])
async def read_items():
    return items
# retorna todos porque no espera un id en la url

# respuesta arbitraria con dict. usar dict, es util si no se conoce los pares como en pydantic
from typing import Dict
from fastapi import FastAPI

app = FastAPI()


@app.get("/keyword-weights/", response_model=Dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}

# código de estado respuestas. declarar el código de estatus.
from fastapi import FastAPI

app = FastAPI()


@app.post("/items/", status_code=201)
async def create_item(name: str):
    return {"name": name}
# otra opción al código de arriba es
from fastapi import FastAPI, status

app = FastAPI()


@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}

# datos de formulario. recibir campos de un formulario en lugar de un JSON
from fastapi import FastAPI, Form

app = FastAPI()


@app.post("/login/")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}

# solicitar achivos. pip3 install python-multipart para enviar los archivos como formularios
from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
# bytes() lee el archivo y lo almacena en memoria, bien para archivos pequeños.
# files solo lee el archivo y retorna el tamaño
"""
ventajas de UploadFile sobre File().
- no se usa File como valor predeterminado
- utiliza un archivo en cola: se almacena en memoria hasta un tamaño maximo, después
de pasar el limite se almacena en disco
- funciona bien par archivos grandes.
- puede obtener metadatos del archivo.

UploadFile tiene los siguientes atributos.
filename: str con el nombre del archivo original.
content-type: str tipo de contenido MIME.
file: SpooledTemporaryFile pasar directamente a otras funciones.

UploadFile tiene metodos async.
write(date): escribe datos (str o bytes).
read(size): lee (int).
seek(offset): va a la posicion de byte (int) en el archivo.
await myfile.read() util si se ejecuta y desea volver a leer el contenido
close(): cierra el archivo
"""
# carga de archivo opcional
from typing import Union
from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(file: Union[bytes, None] = File(default=None)):
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: Union[UploadFile, None] = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}
# en ambos casos el archivo puede ser opcional y debajo hay código que lo valida para retornar un mensaje

# UploadFile con metadatos adicionales con File()
from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(file: bytes = File(description="A file read as bytes")):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(
    file: UploadFile = File(description="A file read as UploadFile"),
):
    return {"filename": file.filename}
# la descripcion es visible en /redoc

# carga de archivos multiples asociados al mismo campo de formulario
from typing import List
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.post("/files/")
async def create_files(files: List[bytes] = File(...)):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile]):
    return {"filenames": [file.filename for file in files]}


@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)

# cargar multiples archivos con metadatos adicionales
from typing import List

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.post("/files/")
async def create_files(
    files: List[bytes] = File(..., description="Multiple files as bytes"),
):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(
    files: List[UploadFile] = File(..., description="Multiple files as UploadFile"),
):
    return {"filenames": [file.filename for file in files]}


@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
# cada formulario (declarado en la ruta / raiz) tiene asignado un metodo post en action

# solicitud de asrchivos y formularios. definir archivos y campos de formulario al mismo tiempo File y From
from fastapi import FastAPI, File, Form, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(
    file: bytes = File(...), fileb: UploadFile = File(...), token: str = Form(...)
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }

# manejo de errores.
# usar HTTPException
from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}
# maneja el eror en caso de no coinidir y devuelve un detalle

# agregar encabezados personalizados para tipos de seguridad.
from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}


@app.get("/items-header/{item_id}")
async def read_item_header(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    return {"item": items[item_id]}

# instalar controladores de excepciones personalizadas.
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


app = FastAPI()


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )


@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}

# configuración operaciones de ruta.
# coódigo de estado de respuesta.
from typing import Set, Union
from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()


@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item
# espera un requests, donde el modelo de entrada sera el de salida

# tags. agregar etiquetas a la ruta de operaciones
from typing import Set, Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()


@app.post("/items/", response_model=Item, tags=["items"])
async def create_item(item: Item):
    return item


@app.get("/items/", tags=["items"])
async def read_items():
    return [{"name": "Foo", "price": 42}]


@app.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]
# son solo tags, fuera de eso no tiene ninguna funcion especial

# etiquetas con enumeración
from enum import Enum
from fastapi import FastAPI

app = FastAPI()


class Tags(Enum):
    items = "items"
    users = "users"


@app.get("/items/", tags=[Tags.items])
async def get_items():
    return ["Portal gun", "Plumbus"]


@app.get("/users/", tags=[Tags.users])
async def read_users():
    return ["Rick", "Morty"]
# tags accede a la enumeracion usando el Clase.atributo_name

# resumen y descripcion. summary y descripcion
from typing import Set, Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()


@app.post(
    "/items/",
    response_model=Item,
    summary="Create an item",
    description="Create an item with all the information, name, description, price, tax and a set of unique tags",
)
async def create_item(item: Item):
    return item

# descripcion de docstring.
from typing import Set, Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()


@app.post("/items/", response_model=Item, summary="Create an item")
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item
# permite markdown y sera visible en docs

# descripcion de respuesta con el parametro response_description
from typing import Set, Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()


@app.post(
    "/items/",
    response_model=Item,
    summary="Create an item",
    response_description="The created item",
)
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item
# la descripcion es visible en docs

# marcar un path ruta como obsoleta
from fastapi import FastAPI

app = FastAPI()


@app.get("/items/", tags=["items"])
async def read_items():
    return [{"name": "Foo", "price": 42}]


@app.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]


@app.get("/elements/", tags=["items"], deprecated=True)
async def read_elements():
    return [{"item_id": "Foo"}]

# condificador compatible con JSON. ej, convertir modelos a dict, list, etc.
# por ejemplo almacenarlo en una base de datos jsonable_encoder() donde datetime debe ser str
# en este caso recibira un dict. RECAP datetime
from datetime import datetime
from typing import Union
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

fake_db = {}


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: Union[str, None] = None


app = FastAPI()


@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data

# body actualizaciones con put. usar jsonable_encoder para coneviertir los valores a su destino.
from typing import List, Union
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: Union[str, None] = None
    description: Union[str, None] = None
    price: Union[float, None] = None
    tax: float = 10.5
    tags: List[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded
# jsonable_encoder convierte los datos de entrada en datos de tipo json, ideal para bases nosql.
# usar los mismos metodos de puts en post, permite ir a la url/item y devoler los valores

# pydantic exclude_unset. recibe actualizaciones parciales item.dict(exclude_unset) omite los valores predeterminados
from typing import List, Union
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: Union[str, None] = None
    description: Union[str, None] = None
    price: Union[float, None] = None
    tax: float = 10.5
    tags: List[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]


@app.patch("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    update_data = item.dict(exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data)
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item
# utiliza el metodo .copy() para realizar el update generando un dict sin valores predeterminados.

"""
dependencias inyeccion de dependencias.
- logic comparativa
- compartir conexion de base de datos
- cumplir requisistos de seguridad, autenticación, roles, etc.
"""
# ejemplo simple
from typing import Union
from fastapi import Depends, FastAPI

app = FastAPI()


async def common_parameters(
    q: Union[str, None] = None, skip: int = 0, limit: int = 100
):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons
# common_parameters espera un argumento q str, un skip opcional o 0 u limit opcional o 100, al final devuelve un dict
# url http://localhost:8000/items/?q=test&skip=0&limit=100
# depends recibe un solo parametro el cual deberia ser una funcion, en este caso common_parameters.
"""
cada vez que llega una nueva solicitud
- llama a la funcion de dependencia confiable de parametros confiables
- obtiene el resultado de la función
- asigna el resultado de la funcion al parametro de path (get)

async y no async.
se puede decalara funciones path async o normales def.
de igual manera para dependencias, no hay problema porque fastapi sabra identificarlo
"""
# la funciones de operación de ruta se usan simpre que una operacion y ruta coinciden
# esto le hace saber a la funcion de path que depende de algo más que debe ejecutarse antes de su funcion
"""
otros terminos
- recursos
- proveedores
- servicios
- inyectables
- componentes

la intregacion y dependencias se puede contruir usando la inyección de dependencias.
esto permite añadir más funcionalidades a los parametros de ruta
"""

# clases como dependencias. cambiar una funcion por una clase
from typing import Union
from fastapi import Depends, FastAPI

app = FastAPI()


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class CommonQueryParams:
    def __init__(self, q: Union[str, None] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@app.get("/items/")
async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response
# se envia en la url, si no recibe el parametro q, retorna los valores predeterminados. retorna clave: valor
# retorna una lista de dict
# se usa dos veces el CommonQueryParams pero el último es el que usa para saber la dependencía que usara
# usar solo una ves el nombre de la dependencia en lugar de dos
from typing import Union
from fastapi import Depends, FastAPI

app = FastAPI()


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class CommonQueryParams:
    def __init__(self, q: Union[str, None] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@app.get("/items/")
async def read_items(commons=Depends(CommonQueryParams)):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response
# el ejemplo de arriba es el mismo pero solo usa una vez la llamada de dependencias.

# sub-dependencias. crear dependencias que tengan sub-dependencias.
from typing import Union
from fastapi import Cookie, Depends, FastAPI

app = FastAPI()


def query_extractor(q: Union[str, None] = None):
    return q


def query_or_cookie_extractor(
    q: str = Depends(query_extractor),
    last_query: Union[str, None] = Cookie(default=None),
):
    if not q:
        return last_query
    return q


@app.get("/items/")
async def read_query(query_or_default: str = Depends(query_or_cookie_extractor)):
    return {"q_or_cookie": query_or_default}
# cookie depende de query_extractor para obtener q, si cookies no recibe nada retorna el valor por defecto y aunque last_query reciba algo
# retornara el valor por defecto

# dependencias en decoradores de operaciones de rutas.
# en algunos casos se necesita ejecutar una dependencia sin devolver el valor de retorno.
# usar una List o list para la dependencia

# agregar dependencias al decorador de operaciones path.
from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()


async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]
# en este caso la dependencias se ejecutaran de la misma manera que una dependencia normal
# pero su valor de pasara por la funcion de path

# dependencías globales. dependencias para todas las aplicaciones
from fastapi import Depends, FastAPI, Header, HTTPException


async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])


@app.get("/items/")
async def read_items():
    return [{"item": "Portal Gun"}, {"item": "Plumbus"}]


@app.get("/users/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]
# en este caso todas las dependencias se aplicán a todas las rutas paths
# ambos paths depedende las 2 dependencias y se debe a que se invovan desde la instancia app

# dependencias de rendimiento yield. dependencias que realizan alguna acción depués de finalizar. usar yield en lugar de return

# crear una dependencia para DB. crear una sesion y cerarla después de terminar
async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()

"""
seguridad (puede llegar a ser complejo).

OAuth2.
especificación que define varias formas de manejar la autenticación y autorización.
incluye formas de autenticación de un tercero para inicio de sesión como FB, TW, G, etc.

OAuth1.
es demaciado compleja ya que inlcuia directamente como encriptar la comunicación.
no es muy popular o usada.
OAuth2 no especifica cifrar la comunicación pero espera ser servido sobre HTTPS

OpenID. no muy popular o usada

OpenAPI (swagger).
opensource parte de la Linux Fundation
FastAPI se base en OpenAPI

OpenAPi define los siguientes esquemas de seguridad.
-- apikey: una clave especifica de la app que puede provenir de:
- un parametro de consulta
- un encabezado
- cookies
-- http: sistema de autenticación HTTP estandar:
- bearer: un encabezado Authorization valor bearer heredaro de OAuth
- autenticación básica HTTP
- resumen HTTP
-- oauth2: todas las formar OAuth2 llamadas 'flujos'
- flujos para crear cliente de autenticación (FB, GH, G, TW, etc)
- implicit
- clientCredential
- authorizacionCode
- flujo especial para manejar la autenticación en la aplicación
password
-- openIdConnect: tiene una forma de descubrir los datos de autenticación de OAuth2

fastapi proporciona fastapi.security que simpifica el uso de los mecanismos de seguridad
"""

# seguridad. suponiendo que se quiere autenticar el frontend con el backend que se encuentran en dominios diferente
# o en un path diferente
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}
# el flujo password es una de las formas OAuth2 para manejar la seguridad y la autenticación.
"""
el proceso seria
- usario escribe user y pass. envia
- envia user y pass atraves de la URL tokenUrl="toker"
- la api comprueba user y pass y responde con un token
un token es una cadena que se puede usar después para verificar el user.
el token esta configurado para caducar después de un tiempo.
por lo que el usuario tendra que iniciar sesion en un tiempo determinado.
si el token es robado no existe mucho riesgo
- la interfaz almacena temporalmente el token en algun lugar
- el usuario ira a otra secciones de la interfaz web
- la interfaz necesitara obtener más datos de la api
necesita autorización para ese endpoint especifico.
para auntenticar con la api, enviara un encabezado Authorization con un valor
Bearer adicional.
si la ficha contiene foobar, el contenido de Authorization en el encabezado seria Bearer foobar
"""
# la instancia OAuth2PasswordBearer obtiene la url que el cliente usara para enviar el user y pass
# que a su vez es una dependencia, al no tener una autorización genera un status code 401

# obtener un usuario actual.
# crear modelo de usurio.
from typing import Union
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
# hay dos depenencias. get_current_user obtiene el usuario actual(sub dependencia es oauth2_scheme) y depende de fake_decode_token (utilidad)
# que es quien llama al modelo User para definir valores
# y todo se manda llamar desde la funcion de ruta el cual es una inyección de la dependencía

# oauth2 con password y Bearer. enviar username y password como datos de formulario (no hay json)
# scope. es una cadena larga separada por espacios
from typing import Union
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

app = FastAPI()


def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
# realmente no genera un hash, lo que hace es concatenar lo que esta en la funcion fake_hash_password junto al password
# lo compara con lo que esta en el dict y en base a la info retorna un error o da acceso al usuario.
# disable indica que usario esta activo o inactivo, esto no le niega el acceso

"""
OAuth2 con contaseña (hashing), Bearer con toker JWT(JSON web token).
es un estandar para codificar un objeto json en una cadena larga, densa y sin espacios.
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c

no está ecriptado, cualquier podría recuperar la información. pero al estar firmado.
con lo cual se puede crear un token con caducidad, por ejemplo una semana.
después de una semana al caducar, el usuario tendra que autenticarse de nuevo
"""
# insalar python-jose[cryptography]
pip3 install python-jose[cryptography]

"""
hashing de contraseñas.
convertir algun contenido en una secuencia de bytes.
cada vez que pasa exactamente el mismo contenido, obtiene lo mismo
pero no se puede converir el datos a contraseña

por qué usar hash de contraseñas.
si alguien roba la base de datos, no tendra las contraseñas de texto, solo los hashes.
"""
# instalar passlib. excelente paquete para manejar hashes de contraseñas
# adminte muchos algoritmos de hash seguros y utilidades para trabajar.
# el algoritmo recomendado es Bcrypt
pip3 install passlib[bcrypt]

# crear un contexto passlib. para codificar y validar contraseñas
# función de utilidad para codificar contreaseñas enviadar por el user
# utilidad para validar la contraseña contra el hash
# y otro para autenticar y devolver el usuario
# crear una secretkey aleatoria para firmar los tokens
openssl rand -hex 32

from datetime import datetime, timedelta
from typing import Union
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "5a4e9f641caf1f11769fbc423822288f26a251561786dbb9feb405261564fcfa"
ALGORITHM = "HS256" # variable con algoritmo para firmar token jwt hs256
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # variable de vencimiento


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

# modelo para usar el token para la respuesta
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# funcion de utilidad para generar un nuevo token
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# actualizar para recibir el mismo token que antes, ahora usando jwt
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# crear un timedelta con el tiempo de expiración
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]
"""
detalles técnicos sobre jwt 'sub'.
jwt dice que hay un sujeto 'sub' con el token.
es opcional pero es ahí donde se coloca la indentificación del usuario.
jwt permite hacer otras cosas ademas de identificar usarios, como realizar operaciones sobre la API.
identificar pubicaciones de blogs.
puede ser usada con bots
"""
pip3 install --upgrade pip
# RECAP sobre oauth2 and fastapi!!!

"""
middleware.
un middleware es una función que funciona con cada solicitud antes de ser procedada
por cualquier operación de ruta. y tambien en cada respuesta antes de devolverlo.
- toma cada solicitud que llega a la aplicación
- luego puede hacer algo con esa solicitud o ejecutar código necesario
- luego pasa la solicitud para que sea procesada en cualquier parte de la aplicación (mediante una ruta de path)
- toma la respuesta generada a traves de la app mediante una operacion de ruta path
- se puede hacer algo con esa respuesta o ejecutar código necesario
- luego devuelve la respuesta.
nota: en dependencias con yield, el código de salida se ejecuta después del middleware.

"""

"""
crear un software. usar el decorador @app.middleware("http").
la función middleware recibe:
- los request
- una función call_next que recibira el request como parametro.
esta función pasara el requests correspondiente a la operación de ruta
luego devuelve el response generada por la operación.
- puede modificar aún más el response antes de devolverlo
"""
import time
from fastapi import FastAPI, Request

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

"""
CORS (cross-origin resource sharing) (intercambio de recursos de origen cruzado)
se refiere a las situaciónes en las que una interfaz que se ejecuta en el navegador
tiene código javascript que se comunica con un backend y el backend está en un origen diferente
a la iterfaz.

Origin. es la combinación de protocolo (http, https), dominio (myapp.com, localhost, localhost.tiangolo.com) y puerto (80, 443, 800)
entondes, todos son origenes diferentes
- http://localhost
- https://localhost
- http:/localhost:8000
incluso estando en localhost, usan diferentes protocolos o puertos.

Steps.
entonces se tiene una interfaz en localhost:8000 y javascript tiene una en localhost
por defecto en el puerto 80 al no especificar.

luego el navegador enviara un solicitud HTTP Options y si el backend envia los encabezados apropiados
que autoricen la comunicación, entonces permitrita la comunicación entre el fron y el back.

para esto el backend debe tener una lista de origenes permitidos
por ejemplo http://localhost:8000

Wildcards
es posible declarar la lista como '*' comodin para permitir todas.
pero solo permite ciertas conexiónes y excluye todo lo que sea credenciales:
cookies, headers de autorización Bearer, tokes, etc.
por lo cual es mejor pasar una lista de origenes.

usar CORSMiddleware
- importart CORSMiddleware
- crear una lista de origenes permitidos (como cadenas)
- como un middleware

si el backend lo permite:
- credenciales (headers, cookies, etc)
- metodos HTTP especificos (POST, PUT) o todos con el comodin '*'
- encabezados especifico con el comodin '*'
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}
"""
(la mayoria espera una lista[])
allow_origins: lista de oirigenes que permite realizar solicitudes cruzadas. (listao '*')
allow_origin_regex: cadena de expresiones regulares para comparar los origenes que se deben permitir.
allow_methods: lista de metodos HTTP, predetermiando GET o '*'.
allow_headers: lista de headers HTTP, predeterminado [] o '*'(permite todos los encabezados).
allow_credentials: indicar las cookies a permitir, predeterminado False. no permite '*', se deben especificar.
expose_headers: indica los encabezados de respuesta que deben estar accesibles para el navegador. predeterminado []
max_age: timepo maximo en segundo para que el navegados almacene en caché la respuesta de CORS. predeterminado a 600.

el middleware responde a dos tipos de solicitudes en particualar HTTP.

solicitudes de verificación previa de CORS.
son cualquier solicitud OPTIONS con Origin y encabezados Access-Control-Rquest-Method.
el middleware interceptara la solicitud entrante y respondera con los encabezados CORS apropiados
y un 200 o 400 con fines informativos.

solicitudes simples
cualquier solicitud con encabezado Origin. pasara la solicitud de forma normal, pero incluira los encabezados CORS apropiados en la respuesta
"""

"""
base de datos (relacionales).
permite usar cualquier tipo de base de datos.

ORM
un patrón común es usar un ORM (mapeo relaciónal de objetos).
un orm tiene herramientas para convertir 'mapa' de objetos en código y tablas de base de datos.

con un ORM, se crea una clase que representa un tabla, cada atributo representa una columna con nombre y tipo.
por ejemplo una clase Pet podría representar una tabla sql pet.
y cada instancía de la clase representa una fila de la DB.

por ejemplo; un objeto orion_cat (instancía de Pet) puede tener un atributo orion_cat.type
para la columan type, y el calor podria ser 'cat'.
cuenta con herramientas para crear conexiones o relaciones de tablas.

así que, orgin_cat.owner.name puede ser name columan de la tabla owner y como valor 'chilaquiles'
"""
# install sqlalchemy
pip3 install sqlalchemy

# trabajar con database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# crea la url para la DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# crea el motor para sqlalchemy
# el argumento connect_args es solo para sqlite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# crea una clase. cada instancia sera una sesion de la DB
# sera la sesión real de la DB. usa la funcion sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# crea una clase Base. sera heredada por los modelos o clases de DB
Base = declarative_base()

# trabajar con models.py
# crea modelos a partir de la clase Base
# models. termino usado para referirse a clases e instancias que interactuan con la DB
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(string)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primeros=True, index=True)
    title = Column(String, index=True)
    descripcion = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
"""
al acceder al atributo item en User, my_user.items, tendra una lista de Item de la tabla items
que tiene un clave foranea que apunta a ese registro en users
entonces al hacer my_user.items, realmente ira y buscara los elementos de items y los traera
y al accedera owner en Item, contendra un modelo de User de la tabla users, usara
el owner_id con la clave foranea y sabra que registros traer de la tabla users
"""

"""
crear los modelos Pydantic. schemas.py
crear ItemBase y UserBase models, para tener atributos comunes al crear o leer datos.

crear ItemCreate y UserCreate que hereda de ellos cualquier dato adicional necesario para la creación.
"""
from typing import List, Union
from pydantic import BaseModel

class ItemBase(BaseModel):
    title: str
    descripcion: Union[str, None] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True
# con orm_mode le dira al modelo que lea incluso si no es un dict, sino un ORM o cualquier otro objeto
# puede obtener un valor id = data["id"] o id = data.id, puede usar el ORM en el response_model

"""
utilidades CRUD. crud.py
funciones reutilizables para interactuar con la DB
CRUD: crear, leer, actualizar y eliminar.

leer datos.
importart Session de sqlalchemy.orm, permite declarar el tipo de paramatro a la DB
mejor verificacion de tipos y finalización en sus funciones
importar model y schemas

funciones de utilidad:
- leer un solo usario por ID y correo
- leer varios usuarios
- leer varios articulos
"""
from sqlalchemy.orm import Session
from . import models, schemas

# obtiene el id del usuario
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# obtiene el email de usuario
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# obtiene todos los usuarios
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limmit(limit).all()

# crear los usuario usando UserCreate de schemas. utilidad
def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=User.email, hashed_password=fake_hash_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# obtiene todos los items
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limite(limit).all()

# crea los items usanndo ItemCreate de schemas. función de utilidad
def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
"""
pasos dentro de las funciones de utilidad.
- modelos SQLALCHEMY con sus datos
- add objeto de instancia a la sesion de DB
- commit realiza los cambios en a DB
- refresh actualiza su instancia
"""

# main.py.
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchem.orm import Session
from . import cru, models, schemas
from .database import SessionLocal, engine

# crear las tablas para la DB
model.Base.metadata.create_all(bind=engine)

app = FastAPI()

# dependencias
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# la respuesa es igual a lo que se ingresa
# db_user obtiene el email
# si ya existe retorna una excepción
# de lo contrario crea el usuario
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session, = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email ya registrado!")
    return crud.crear_user(db=db, user=user)


# la respuesta sera una lisa de todos los users obtenidos
# la función dentro de la dependencia no nesecita (), es un invocable
# users es igual a los resultado de la consulta de get_users
@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


# retorna solo un usuario
# espera un user_id
# si es usario no esta en la DB retorna una excepción
# si no, retorna el usario perteneciente de ese id
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user id None:
        raise HTTPException(status_code=400, detail="User not found!")
    return db_user


# espera un user_id del cual se quiera crear un item
# manda llamar a ItemCreate para usar el model
# crear un item para el usuario y al mismo tiempo crear la relación
@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


# retorna una lista de todos los items
@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
"""
Alembic
una migración es el conjunto de pasos necesarios cada vez que cambia la estructura de los modelos
SQLALCHEMY, agrega un nueco atributo, etc. replica los cambios en la DB añadiendo la nueva columan, tabla, etc.
"""
# ejecutar
uvicorn sql_app.main:app --reload

# Multiples archivos
# APIRouter. /app/routers/users.py dedicado a menajar los usuarios
# app/routers/users.py
from fastapi import APIRouter

router = APIRouter()


@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
# APIRouter es como un mini FastAPI

# app/dependencies.py
from fastapi import Header, HTTPException


async def get_token_header(x_token: str = Header()):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")

"""
app/routers/items.py endpoint para manejar 'elementos'
tiene operaciones de ruta para
- /items/
- /items/{item_id}
en la instancia router si colocan los parametros que seran usados por todos les metodos de ruta
"""
from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_token_header

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


@router.get("/")
async def read_items():
    return fake_items_db


@router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}


@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}


# app/main.py
from fastapi import Depends, FastAPI
from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users

app = FastAPI(dependencies=[Depends(get_query_token)])


app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

# app/internal/admin.py
from fastapi import APIRouter

router = APIRouter()


@router.post("/")
async def update_admin():
    return {"message": "Admin getting schwifty"}


# tareas en segundo plano
"""
definir tareas en segundo plano que se ejecuten despues de devolver una respuesta
por ejemplo:
- notificar por correo después de una acción
- procesando datos
"""
# usando BackgroundTasks
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}

# archivos estaticos usando StaticFiles
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Testing
# usando TestClient
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
# pruebas extendidas
# main.py
from typing import Union
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

fake_secret_token = "coneofsilence"

fake_db = {
    "foo": {"id": "foo", "title": "Foo", "description": "There goes my hero"},
    "bar": {"id": "bar", "title": "Bar", "description": "The bartenders"},
}

app = FastAPI()


class Item(BaseModel):
    id: str
    title: str
    description: Union[str, None] = None


@app.get("/items/{item_id}", response_model=Item)
async def read_main(item_id: str, x_token: str = Header(...)):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_db[item_id]


@app.post("/items/", response_model=Item)
async def create_item(item: Item, x_token: str = Header(...)):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if item.id in fake_db:
        raise HTTPException(status_code=400, detail="Item already exists")
    fake_db[item.id] = item
    return item

# test_main.py
from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)


def test_read_item():
    response = client.get("/items/foo", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == {
        "id": "foo",
        "title": "Foo",
        "description": "There goes my hero",
    }


def test_read_item_bad_token():
    response = client.get("/items/foo", headers={"X-Token": "hailhydra"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_read_inexistent_item():
    response = client.get("/items/baz", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_create_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={"id": "foobar", "title": "Foo Bar", "description": "The Foo Barters"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "foobar",
        "title": "Foo Bar",
        "description": "The Foo Barters",
    }


def test_create_item_bad_token():
    response = client.post(
        "/items/",
        headers={"X-Token": "hailhydra"},
        json={"id": "bazz", "title": "Bazz", "description": "Drop the bazz"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_create_existing_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={
            "id": "foo",
            "title": "The Foo ID Stealers",
            "description": "There goes my stealer",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Item already exists"}


# debugging https://fastapi.tiangolo.com/tutorial/debugging/
# para el proceso de nginx con supervisord.
# install
sudo apt install nginx supervisor -y
# creados los archivos de configuración
sudo systemclt restart nginx
sudo supervisorctl reload
# puede marcar error porque otro proceso esta corriendo con el mismo puerto
sudo supervisord -c /etc/supervisor/conf.d/fastapi.conf
# detener
pgrep "supervisor" -a
sudo kill num_pid
# debe correr bien
sudo supervisord -c /etc/supervisor/conf.d/fastapi.conf
