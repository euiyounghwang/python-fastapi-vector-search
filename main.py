from fastapi import FastAPI, Request
# from config.log_config import create_log
from injector import (logger, doc)
from openapi.api_model import Item, Search
from controller.api_controller import (api_controller)
import json


app = FastAPI()

@app.get("/v1/basic")
# async def root():
def api():
    return {"message": "Hello World"}


@app.get("/v1/basic/api/{id}")
def get(id:str):
    return {"message": "Hello your id {}".format(id)}


@app.post("/v1/basic/search")
async def Elasticsearch_Search(request: Search):
    response_json = await api_controller(request)
    return response_json


@app.post("/v1/basic/vector_search")
async def Vector_Search(item: Item):
    response_json = await api_controller(item)
    return response_json