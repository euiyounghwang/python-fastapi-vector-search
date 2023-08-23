
from pydantic import BaseModel

class Item(BaseModel):
    process_id: int
    price: int
    name: str
    