from enum import Enum

class UserRole(str, Enum):
  admin = 'admin'
  client = 'client'
  delivery = 'delivery'