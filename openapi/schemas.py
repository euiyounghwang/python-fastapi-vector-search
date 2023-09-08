from pydantic import BaseModel, Field, NonNegativeInt, validator
from datetime import datetime
from pytz import timezone as tz
from enum import Enum
from typing import List, Union

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
    query_string: str = "video"
    size: int = 20
    # sort_order: str = "DESC"
    sort_order: Sort_Order = Sort_Order.desc
    start_date : str = "2021 01-01 00:00:00"
    
    
class NoteSchema(BaseModel):
    # id: uuid.UUID
    title: str = Field(..., min_length=3, max_length=50) #additional validation for the inputs 
    description: Union[str, None] = None
    completed: str = "False"
    created_at: datetime
    # created_date: str = dt.now(tz("Africa/Nairobi")).strftime("%Y-%m-%d %H:%M")
    
    
    # description: Optional[str] = None
    # price: float
    # tax: Optional[float] = None
    
    class Config:
        orm_mode = True
       
    @validator("title", "description")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Not allow to value for empty')
        return v
    
    @validator("title", "description")
    def not_default(cls, v):
        if v.strip() == "string":
            raise ValueError('Not allow to value for string')
        return v

class NoteDB(NoteSchema):
    id: int 
    
class Note_Sub_Entity(BaseModel):
    pass