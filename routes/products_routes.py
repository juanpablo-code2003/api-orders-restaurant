import time

from fastapi import APIRouter, Path, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List

from middlewares.permission_user import UserPermission
from config.database import SessionDB
from models.product_model import Product
from schemas.product_schemas import ProductSchema


products_router = APIRouter()

tags = ['Products']

@products_router.get(
  '/products', 
  tags=tags, 
  response_model=List[ProductSchema], 
  status_code=200, 
  dependencies=[Depends(UserPermission())]
)
def get_all_products() -> List[ProductSchema]:
  db = SessionDB()
  products = db.query(Product).all()
  return JSONResponse(content=jsonable_encoder(products), status_code=200)

@products_router.get(
  '/products/{id}', 
  tags=tags, 
  response_model=ProductSchema, 
  status_code=200, 
  dependencies=[Depends(UserPermission())]
)
def get_product_by_id(id: int):
  db = SessionDB()
  product = db.query(Product).filter(Product.id == id).first()
  response = JSONResponse(content=jsonable_encoder(product), status_code=200)
  if not product:
    response = JSONResponse(content={'message': 'Movie not found'}, status_code=404)
    
  return response