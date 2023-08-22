from fastapi import FastAPI, Request
from pydantic import BaseModel
import json


app = FastAPI()

class Item(BaseModel):
    process_id: int
    
@app.get("/")
# async def root():
def api():
    return {"message": "Hello World"}


@app.get("/api/{id}")
def get(id:str):
    return {"message": "Hello your id {}".format(id)}


@app.post("/api")
async def root(item: Item):
    print(item, type(item), item.process_id, [{"process_id" : v} for k, v in item])
    return item