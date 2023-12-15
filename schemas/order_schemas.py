from pydantic import BaseModel, conlist

from schemas.item_order_schemas import ItemOrderSchema, CreateItemOrderSchema
from models.order_model import StatesOrder

class OrderSchema(BaseModel):
  id: int
  client_id: int
  delivery_id: int
  date: str
  total: int
  state: str
  items: conlist(ItemOrderSchema, min_length=1) 
  
class CreateOrderSchema(BaseModel):
  items: conlist(CreateItemOrderSchema, min_length=1)
  
class UpdateStateOrderSchema(BaseModel):
  state: StatesOrder
  
