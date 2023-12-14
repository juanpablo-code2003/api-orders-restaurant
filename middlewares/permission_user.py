from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer

from utils.jwt_manager import validate_token
from config.database import SessionDB
from models.user_model import User

class UserPermission(HTTPBearer):
  def __init__(self, *roles: str):
    super().__init__()
    self.roles = roles
    
  async def __call__(self, request: Request):
    auth = await super().__call__(request)
    data = validate_token(auth.credentials)

    if data is None:
      raise HTTPException(status_code=401, detail='Invalid token')
    
    db = SessionDB()
    user = db.query(User).filter(User.id == data.get('id')).first()
    
    if not user:
      raise HTTPException(status_code=401, detail='Invalid user')
    
    if len(self.roles) != 0 and self.roles[0] != 'all' and user.role not in self.roles:
      raise HTTPException(status_code=403, detail='You do not have permission to access this resource')
    
    return user