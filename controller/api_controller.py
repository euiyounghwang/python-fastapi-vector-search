

from fastapi import APIRouter, Depends

from openapi.schemas import Item, Search, NoteSchema
from prometheus_client import Counter, Histogram
from basic import api_request_counter, api_request_summary
from injector import (logger, doc)

from sqlalchemy.orm import Session
from openapi.database import get_db
# from fastapi_pagination import LimitOffsetPage, add_pagination, paginate

# from openapi.repository import get_all
import openapi.repository as repository
import json

app = APIRouter(
    # prefix="/Note",
)


ITEM_NOT_FOUND = "Item not found for id: {}"


@app.post("/Note", description="create")
async def create(request: NoteSchema, db: Session = Depends(get_db)):
    request_json = {k : v for k, v in request}
    print(request, type(request), request_json)
    # logger.info("create : {}".format(json.dumps(request_json, indent=2)))
    status_code = await repository.create(request, db)
    if status_code == 201:
        return {"message " : "OK - Successful search executed"}
    elif status_code == 202:
        return {"message " : "Warning - existing.."}
    return request_json


@app.get("/Note")
async def get(db: Session = Depends(get_db)):
    list_all = await repository.fetchAll(db)
    return list_all


@app.get("/Note/{id}")
async def fetchById(_id, db: Session = Depends(get_db)):
    note_data = await repository.fetchById(_id, db)
    if note_data:
        print('fetchById (seq) -> ', note_data)
        return note_data.json()
    return {'message': ITEM_NOT_FOUND.format(id)}, 404
