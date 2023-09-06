import os

from sqlalchemy import (Column, Integer, String, Table, create_engine, MetaData, UniqueConstraint, ForeignKey)
from sqlalchemy.dialects.mysql import SMALLINT, TINYINT, BIGINT, CHAR
from openapi.database import Base
from datetime import datetime as dt
from pytz import timezone as tz


class Notes(Base):
    __tablename__ = "notes"
    
    # id = Column(Integer, primary_key=True, index=True)
    # title = Column(String, index=True)
    # description = Column(String)
    # completed = Column(String, nullable=False)
    # created_date = Column(String,default=dt.now(tz("Africa/Nairobi")).strftime("%Y-%m-%d %H:%M"))
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    description = Column(String(50))
    completed = Column(String(8), nullable=False)
    created_date = Column(String(30),default=dt.now(tz("Africa/Nairobi")).strftime("%Y-%m-%d %H:%M"))
    
    def __repr__(self):
        return 'NotesModel(id=%d,title=%s,description=%s,completed=%s,)' % (self.id, self.title, self.description, self.completed)

    def json(self):
        return {'id':self.id,'title': self.title, 'description': self.description, 'completed': self.completed}


class Note_Sub_Entity(Base):
    __tablename__ = "Note_Sub_Entity"
    # __table_args__ = (UniqueConstraint("schema_name", "table_name", name="schema_table_uq_constraint"),)

    table_no = Column(BIGINT(20), primary_key=True, autoincrement=True, nullable=False)
    db_id = Column(Integer, ForeignKey("notes.id"), nullable=False, comment="DB ID")
    sub_description = Column(String(50))