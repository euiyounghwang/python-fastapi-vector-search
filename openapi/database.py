import os

from sqlalchemy import (create_engine, MetaData)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()