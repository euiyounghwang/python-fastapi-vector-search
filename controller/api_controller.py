

from fastapi import APIRouter
from openapi.schemas import Item, Search, NoteSchema
from prometheus_client import Counter, Histogram
from basic import api_request_counter, api_request_summary
from injector import (logger, doc)
import json

app = APIRouter(
    prefix="/Note",
)



@app.post("/create")
async def create(request: NoteSchema):
    request_json = {k : v for k, v in request}
    print(request, type(request), request_json)
    logger.info("create : {}".format(json.dumps(request_json, indent=2)))
    return {"okay" : "1"}
