from fastapi import FastAPI, Request
# from config.log_config import create_log
from injector import (logger, doc)
from openapi.model import *
from controller.api_controller import (api_controller)
import json


app = FastAPI()

@app.get("/")
# async def root():
def api():
    return {"message": "Hello World"}


@app.get("/api/{id}")
def get(id:str):
    return {"message": "Hello your id {}".format(id)}


@app.post("/api")
async def request_api(item: Item):
    response_json = await api_controller(item)
    return response_json