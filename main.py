import time

from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse

from config.database import engine, Base
from middlewares.permission_user import UserPermission
from middlewares.error_handler import ErrorHandler
from routes.auth_routes import auth_router
from routes.products_routes import products_router

from models.item_order_model import *
from models.order_model import *
from models.user_model import *
from models.product_model import *

app = FastAPI()

app.title = 'Pedidos Restaurante'
app.description = 'API de pedidos de restaurante'
app.version = '1.0.0'

app.add_middleware(ErrorHandler)
app.include_router(auth_router)
app.include_router(products_router)

Base.metadata.create_all(engine)


@app.get('/', tags=['Home'])
def home(user: User = Depends(UserPermission())):
  return HTMLResponse(
    content=f'<h1>Bienvenido a FASTAPI restaurant usuario {user.email}</h1>', 
    status_code=200
  )


