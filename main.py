'''
Archivo main de la aplicación. 
Aquí se configura la aplicación y se registran las rutas.

Author: Juan Pablo Garcia Montes
Date: 2023-12-15
Version: 1.0
'''

from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse

from config.database import engine, Base
from middlewares.permission_user import UserPermission
from middlewares.error_handler import ErrorHandler

from routes.auth_routes import auth_router
from routes.products_routes import products_router
from routes.product_lines_routes import product_lines_router
from routes.orders_routes import orders_router

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
app.include_router(product_lines_router)
app.include_router(products_router)
app.include_router(orders_router)

Base.metadata.create_all(engine)


@app.get('/', tags=['Home'])
def home(user: User = Depends(UserPermission())):
  return HTMLResponse(
    content=f'<h1>Bienvenido a FASTAPI restaurant usuario {user.email}</h1>', 
    status_code=200
  )


