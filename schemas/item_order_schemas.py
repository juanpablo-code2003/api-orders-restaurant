from pydantic import BaseModel

class ItemOrderSchema(BaseModel):
  id: int
  product_id: int
  order_id: int
  quantity: int
  
class CreateItemOrderSchema(BaseModel):
  product_id: int
  quantity: int