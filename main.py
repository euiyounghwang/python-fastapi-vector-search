from fastapi import FastAPI, Request
from pydantic import BaseModel
from config.log_config import create_log
import json


logger = create_log()
app = FastAPI()

class Item(BaseModel):
    process_id: int
    price: int
    name: str
    
@app.get("/")
# async def root():
def api():
    return {"message": "Hello World"}


@app.get("/api/{id}")
def get(id:str):
    return {"message": "Hello your id {}".format(id)}


@app.post("/api")
async def request_api(item: Item):
    request_json = [{k : v} for k, v in item]
    print(item, type(item), item.process_id, request_json)
    logger.info("request : {}".format(json.dumps(request_json, indent=2)))
    return item