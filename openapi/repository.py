
from sqlalchemy.orm import Session
from openapi.models import Notes
# from openapi.schemas import NoteSchema
import openapi.models
from injector import (logger, doc)
import json
from controller.Handler.StatusHanlder import StatusHanlder

async def fetchAll(db: Session):
    return db.query(Notes).all()


async def fetchById(_id, db: Session):
    return db.query(Notes).filter(Notes.id == _id).first()


async def deleteById(_id, db: Session):
    is_row = db.query(Notes).filter(Notes.id == _id).first()
    if is_row:
        print("{} is exist...now deleting".format(_id))
        # note_data = Notes(id=_id)
        db.delete(is_row)
        db.commit()
        return StatusHanlder.HTTP_STATUS_200
    return StatusHanlder.HTTP_STATUS_404


async def update(note, db: Session):
    print('update -> ', note)
    db.merge(note)
    db.commit()
    return StatusHanlder.HTTP_STATUS_200

    
async def create(note, db: Session):
    print('create -> ', note)
    is_row = db.query(Notes).filter(Notes.title==note.title).first()
    if is_row:
        return StatusHanlder.HTTP_STATUS_202
    
    note_data = Notes(title=note.title, description=note.description, completed=note.completed, created_date=note.created_date)
    db.add(note_data)
    db.commit()
    print('Created..')
    logger.info(json.dumps(note_data.json(), indent=2))
    return StatusHanlder.HTTP_STATUS_200
    
