from pydantic import BaseModel, Field, NonNegativeInt, validator
from datetime import datetime
from pytz import timezone as tz
from enum import Enum
from typing import List, Union
import uuid

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
    
    def to_json(self):
        return {
            'include_basic_aggs' : self.include_basic_aggs,
            'pit_id' : self.pit_id,
            'query_string' : self.query_string,
            'size' : self.size,
            'sort_order' : self.sort_order,
            'start_date' : self.start_date,
        }
    
    
class NoteSchema(BaseModel):
    # id: uuid.UUID
    title: str = Field(..., min_length=3, max_length=50) #additional validation for the inputs 
    description: Union[str, None] = None
    completed: str = "False"
    # created_at: datetime
    # created_date: str = dt.now(tz("Africa/Nairobi")).strftime("%Y-%m-%d %H:%M")
    
    
    # description: Optional[str] = None
    # price: float
    # tax: Optional[float] = None
    
    class Config:
        # * 'orm_mode' has been renamed to 'from_attributes'
        # orm_mode = True
        from_attributes = True
       
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


class NoteResponse(NoteSchema):
    id: uuid.UUID
    title: str
    description: str
    created_at: datetime
    updated_at: datetime


class NoteResponseSchema(BaseModel):
    Total: int
    Results: List[NoteResponse]
    
    
class RedisResponse(BaseModel):
    KEY: str
    REQUEST_USER_ID: str
    OBJECT_V: str
    INPUT_DATE: str
    EXPIRED_SECONDS: float
    
class RedisResponseSchema(BaseModel):
    Total: int
    Results: List[RedisResponse]    


class NoteDB(NoteSchema):
    id: int 
    
class Note_Sub_Entity(BaseModel):
    pass


class MessageSchema(BaseModel):
    message: str