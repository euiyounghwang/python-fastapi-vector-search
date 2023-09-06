import os

from sqlalchemy import (Column, Integer, String, Table, create_engine, MetaData)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
# from databases import Database
from datetime import datetime as dt
from pytz import timezone as tz
# from db.base_class import Base

load_dotenv()
# Database url if none is passed the default one is used
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:1234@localhost:15432/postgres")

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Session = sessionmaker()
# Session.configure(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


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
