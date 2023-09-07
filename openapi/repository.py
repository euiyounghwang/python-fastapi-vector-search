
from sqlalchemy.orm import Session
from openapi.models import Notes
# from openapi.schemas import NoteSchema
import openapi.models

async def fetchAll(db: Session):
    return db.query(Notes).all()

async def fetchById(_id, db: Session):
    return db.query(Notes).filter(Notes.id == _id).first()


async def create(note, db: Session):
    print('create -> ', note)
    is_row = db.query(Notes).filter(Notes.title==note.title).first()
    if is_row:
        print("{} is exist...".format(note.title))
        return 202
    
    note_data = Notes(title=note.title, description=note.description, completed=note.completed, created_date=note.created_date)
    db.add(note_data)
    db.commit()
    return 201
    
