from pydantic import BaseModel, Field
from typing import Optional

class BaseProductSchema(BaseModel):
  name: str = Field(max_length=50)
  price: int
  
class CreateProductSchema(BaseProductSchema):
  product_line_id: int
  
class ProductSchema(BaseProductSchema):
  id: int
  product_line_id: int
  
  
class ProductLineSchema(BaseModel):
  id: int
  name: str = Field(max_length=30)
  
class CreateProductLineSchema(BaseModel):
  name: str = Field(max_length=30)