from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from utils.jwt_manager import validate_token

from config.database import SessionDB
from models.user_model import User

class JWTBearer(HTTPBearer):
  async def __call__(self, request: Request):
    auth = await super().__call__(request)
    data = validate_token(auth.credentials)

    if data is None:
      raise HTTPException(status_code=401, detail='Invalid token')
    
    db = SessionDB()
    user = db.query(User).filter(User.email == data['email']).first()
    
    if not user:
      raise HTTPException(status_code=401, detail='Invalid user')
    
    return user