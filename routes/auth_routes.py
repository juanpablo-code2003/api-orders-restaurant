from fastapi import APIRouter
from fastapi.responses import JSONResponse

from utils.jwt_manager import create_token
from schemas.user_schemas import LoginSchema, UserSchema
from config.database import SessionDB
from models.user_model import *
from utils.hashing import hash_password

auth_router = APIRouter()

tags = ['Auth']


@auth_router.post('/login', tags=tags, response_model=dict, status_code=200)
def login(user: LoginSchema):
  db = SessionDB()
  logged_user = db.query(User).filter(User.email == user.email, User.password == hash_password(user.password)).first()
  
  if logged_user:
    data_token = {'id': logged_user.id, 'role': logged_user.role}
    
    token = create_token(data=data_token)
    response = JSONResponse(
      content={'message': 'Login success', 'token': token}, 
      status_code=200
    )
  else:
    response = JSONResponse(
      content={'message': 'Login failed'}, 
      status_code=401
    )
    
  return response



@auth_router.post('/register', tags=tags, response_model=dict, status_code=201)
def register(user: UserSchema):
  db = SessionDB()
  new_user = roles_user.get(user.role)(**user.model_dump())
  new_user.password = hash_password(new_user.password)
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  
  return JSONResponse(
    content={'message': 'User created successfully'}, 
    status_code=201
  )