from pydantic import BaseModel, Field, NonNegativeInt
from datetime import datetime as dt
from pytz import timezone as tz
from enum import Enum

# --
# API Model
# --

class Item(BaseModel):
    process_id: int
    price: int
    name: str
    

class Sort_Order(str, Enum):
    desc = 'DESC'
    asc = 'ASC'
    
    
class Search(BaseModel):
    include_basic_aggs: bool = True
    pit_id: str = ""
    query_string: str = "Cryptocurrency"
    size: int = 20
    # sort_order: str = "DESC"
    sort_order: Sort_Order = Sort_Order.desc
    start_date : str = "2021 01-01 00:00:00"
    
    
class NoteSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=50) #additional validation for the inputs 
    description: str = Field(...,min_length=3, max_length=50)
    completed: str = "False"
    created_date: str = dt.now(tz("Africa/Nairobi")).strftime("%Y-%m-%d %H:%M")
    
    class Config:
        orm_mode = True

class NoteDB(NoteSchema):
    id: int 