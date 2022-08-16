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
