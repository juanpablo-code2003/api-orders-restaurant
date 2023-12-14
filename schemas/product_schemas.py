from pydantic import BaseModel, Field
from typing import Optional

class ProductSchema(BaseModel):
  id: int
  email: str
  password: str = Field(min_length=8)
  role: str