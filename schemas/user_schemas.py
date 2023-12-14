from pydantic import BaseModel, Field
from typing import Optional

from constants.user_roles import UserRole

class LoginSchema(BaseModel):
  email: str
  password: str = Field(min_length=8)

class UserSchema(BaseModel):
  email: str
  password: str = Field(min_length=8)
  role: UserRole