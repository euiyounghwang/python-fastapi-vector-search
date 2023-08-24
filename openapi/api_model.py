
from pydantic import BaseModel
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

    
    

    