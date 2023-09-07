

from fastapi import APIRouter, Depends, HTTPException

from openapi.schemas import Item, Search, NoteSchema
from prometheus_client import Counter, Histogram
from basic import api_request_counter, api_request_summary
from injector import (logger, doc)

from sqlalchemy.orm import Session
from openapi.database import get_db
# from fastapi_pagination import LimitOffsetPage, add_pagination, paginate

from controller.Handler.StatusHanlder import StatusHanlder

# from openapi.repository import get_all
import openapi.repository as repository
import json

app = APIRouter(
    # prefix="/Note",
)


ITEM_NOT_FOUND = "Item not found for id: {}"


@app.post("/Note", description="Create a new Item", summary="Create a new Item")
async def create(request: NoteSchema, db: Session = Depends(get_db)):
    request_json = {k : v for k, v in request}
    print(request, type(request), request_json)
    # logger.info("create : {}".format(json.dumps(request_json, indent=2)))
    status_code = await repository.create(request, db)
    if status_code == StatusHanlder.HTTP_STATUS_200:
        return {"message " : "OK - Successful Query executed"}
    elif status_code == 202:
        return {"message " : "Warning - existing.."}
    return request_json


@app.put("/Note/{id}", description="Update an Item with given ID", summary="Update an Item with given ID")
async def update(_id, request: NoteSchema, db: Session = Depends(get_db)):
    request_json = {k : v for k, v in request}
    print(request, type(request), request_json)
    logger.info("update : {}".format(json.dumps(request_json, indent=2)))
    note_data = await repository.fetchById(_id, db)
    if note_data:
        print('update in controller -> ', request_json)
        note_data.title = request_json["title"]
        note_data.description = request_json["description"]
        status_code = await repository.update(note_data, db)
        if status_code == StatusHanlder.HTTP_STATUS_200:
            return {"message " : "OK - Successful Query executed"}
    raise HTTPException(status_code=StatusHanlder.HTTP_STATUS_404, detail={'message': ITEM_NOT_FOUND.format(_id)})


@app.get("/Note", description="Returns a list of items", summary="Returns a list of items")
async def get(db: Session = Depends(get_db)):
    note_data = await repository.fetchAll(db)
    if note_data:
        print(note_data, type(note_data))
        noteRepo = [obj.json() for obj in note_data]
        print(noteRepo, type(noteRepo))
        return noteRepo
    raise HTTPException(status_code=StatusHanlder.HTTP_STATUS_404, detail={'message': ITEM_NOT_FOUND.format(_id)})


@app.get("/Note/{id}", description="Return an Item with given ID", summary="Return an Item with given ID")
async def fetchById(_id, db: Session = Depends(get_db)):
    note_data = await repository.fetchById(_id, db)
    if note_data:
        print("fetchById - > {}".format(_id))
        logger.info(json.dumps(note_data.json(), indent=2))
        return note_data.json()
    
    raise HTTPException(status_code=StatusHanlder.HTTP_STATUS_404, detail={'message': ITEM_NOT_FOUND.format(_id)})
    

@app.delete("/Note/{id}", description="Deleted an Item with given ID", summary="Deleted an Item with given ID")
async def deleteById(_id, db: Session = Depends(get_db)):
    note_data = await repository.deleteById(_id, db)
    if note_data:
        print('deleteById -> ', note_data)
        return {'message': 'Item deleted successfully'}
    raise HTTPException(status_code=StatusHanlder.HTTP_STATUS_404, detail={'message': ITEM_NOT_FOUND.format(_id)})
