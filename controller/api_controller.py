

from fastapi import APIRouter, Depends, HTTPException

from openapi.schemas import (Item, Search, NoteSchema, NoteResponseSchema)
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
    # prefix="/api",
)


ITEM_NOT_FOUND = "Item not found for id: {}"
ITEM_NOT_FOUND_ALL = "Item not found all"


@app.post("/Note", 
          status_code=StatusHanlder.HTTP_STATUS_200,
          description="Create a new Item", 
          summary="Create a new Item")
async def create(request: NoteSchema, db: Session = Depends(get_db)):
    request_json = {k : v for k, v in request}
    print(request, type(request), request_json)
    # logger.info("create : {}".format(json.dumps(request_json, indent=2)))
    status_code, created_uuid = await repository.create(request, db)
    if status_code == StatusHanlder.HTTP_STATUS_200:
        return {"message " : "OK - Successful Query executed", "uuid" : created_uuid}
    elif status_code == 202:
        return {"message " : "Warning - existing.."}
    return request_json


@app.put("/Note/{id}", 
         status_code=StatusHanlder.HTTP_STATUS_200, 
         description="Update an Item with given ID", 
         summary="Update an Item with given ID")
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
    raise HTTPException(status_code=StatusHanlder.HTTP_STATUS_404, detail={'message': ITEM_NOT_FOUND.format(id)})


# --
# http://localhost:7000/Note?limit=10&page=1
# --
@app.get("/Note", 
         response_model=NoteResponseSchema, 
         status_code=StatusHanlder.HTTP_STATUS_200,
         description="Returns a list of items", 
         summary="Returns a list of items")
async def get_all(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ""):
    skip = (page - 1) * limit
    note_data, totalRepo = await repository.fetchAll(db, skip, limit, search)
    if note_data:
        print(note_data, type(note_data))
        noteRepo = [obj.json() for obj in note_data]
        print(noteRepo, type(noteRepo))
        return {"Total": len(totalRepo), "Results": noteRepo}
    raise HTTPException(status_code=StatusHanlder.HTTP_STATUS_404, detail={'message': ITEM_NOT_FOUND_ALL})


@app.get("/Note/{id}", 
         status_code=StatusHanlder.HTTP_STATUS_200,
         description="Return an Item with given ID", 
         summary="Return an Item with given ID")
async def fetchById(id, db: Session = Depends(get_db)):
    note_data, data_all = await repository.fetchById(id, db)
    if note_data:
        print("fetchById - > {}".format(id))
        logger.info(json.dumps(note_data.json(), indent=2))
        return {"Total": len(data_all), "Results": note_data.json()}
        # return note_data.json()
    
    raise HTTPException(status_code=StatusHanlder.HTTP_STATUS_404, detail={'message': ITEM_NOT_FOUND.format(id)})
    

@app.delete("/Note/{id}",
            status_code=StatusHanlder.HTTP_STATUS_200, 
            description="Deleted an Item with given ID", 
            summary="Deleted an Item with given ID")
async def deleteById(id, db: Session = Depends(get_db)):
    status_code = await repository.deleteById(id, db)
    if status_code == 200:
        print('deleteById -> ', id)
        return {'message': 'Item: {} was deleted successfully'.format(id)}
    raise HTTPException(status_code=StatusHanlder.HTTP_STATUS_404, detail={'message': ITEM_NOT_FOUND.format(id)})
