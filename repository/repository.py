
from sqlalchemy.orm import Session
from repository.models import Notes
# from openapi.schemas import NoteSchema
import repository.models
from injector import (logger, doc)
import json
from service.Handler.search.StatusHanlder import StatusHanlder
from sqlalchemy import and_, or_, not_
# from repository.reposistory_interface import RepositoryInterface


# --
# repository.py — Database Service layer
# --

class NoteRepository(object):

    async def fetchAll(self, db: Session, skip, limit, search):
        logger.info("fetchAll - skip: {}, limit: {}, search: {}".format(skip, limit, search))
        if search:
            results_repo = db.query(Notes) \
                    .filter(or_(Notes.title.contains(search), Notes.description.contains(search))) \
                    .limit(limit) \
                    .offset(skip) \
                    .all()
            noteRepo = [obj.json() for obj in results_repo]
            logger.info("Repo from Postgres: {}".format(json.dumps(noteRepo, indent=2)))
            return results_repo, \
                db.query(Notes) \
                    .filter(or_(Notes.title.contains(search), Notes.description.contains(search))) \
                    .all()
        else:
            print('@#$%%')
            results_repo = db.query(Notes) \
                    .limit(limit) \
                    .offset(skip) \
                    .all()
            noteRepo = [obj.json() for obj in results_repo]
            logger.info("Repo from Postgres: {}".format(json.dumps(noteRepo, indent=2)))
            return results_repo, \
                db.query(Notes) \
                    .all()

    async def fetchById(self, _id, db: Session):
        logger.info("fetchById - {}".format(_id))
        return db.query(Notes).filter(Notes.id == _id).first(), db.query(Notes).filter(Notes.id == _id).all()


    async def deleteById(self, _id, db: Session):
        is_row = db.query(Notes).filter(Notes.id == _id).first()
        if not is_row:
            return StatusHanlder.HTTP_STATUS_404
        logger.info("{} is exist...now deleting".format(_id))
        # note_data = Notes(id=_id)
        db.delete(is_row)
        db.commit()
        return StatusHanlder.HTTP_STATUS_200
        
        
    async def update(self, note, db: Session):
        logger.info('update -> {}'.format(note))
        db.merge(note)
        db.commit()
        return StatusHanlder.HTTP_STATUS_200


    async def create(self, note, db: Session):
        '''
        is_row = db.query(Notes).filter(Notes.title==note.title).first()
        if is_row:
            return StatusHanlder.HTTP_STATUS_202
        '''
        note_data = Notes(title=note.title, description=note.description, completed=note.completed)
        db.add(note_data)
        db.commit()
        logger.info('create -> {}'.format(note_data.id))
        logger.info(json.dumps(note_data.json(), indent=2))
        
        return StatusHanlder.HTTP_STATUS_200, note_data.id
    
