'''
Manejo de las rutas de productos.

Author: Juan Pablo Garcia Montes
Date: 2023-12-15
Version: 1.0
'''

from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List

from middlewares.permission_user import UserPermission
from config.database import SessionDB
from models.product_model import Product, ProductLine
from schemas.product_schemas import ProductSchema, CreateProductSchema


products_router = APIRouter()

tags = ['Products']

@products_router.get(
  '/products', 
  tags=tags, 
  response_model=List[ProductSchema], 
  status_code=200, 
  dependencies=[Depends(UserPermission('all'))]
)
def get_all_products() -> List[ProductSchema]:
  '''Get all products for all users'''
  db = SessionDB()
  products = db.query(Product).all()
  return JSONResponse(content=jsonable_encoder(products), status_code=200)

@products_router.get(
  '/products/{id}', 
  tags=tags, 
  response_model=ProductSchema, 
  status_code=200, 
  dependencies=[Depends(UserPermission('all'))]
)
def get_product_by_id(id: int):
  '''Get product by id for all users'''
  db = SessionDB()
  product = db.query(Product).filter(Product.id == id).first()
  response = JSONResponse(content=jsonable_encoder(product), status_code=200)
  if not product:
    response = JSONResponse(content={'message': 'Product not found'}, status_code=404)
    
  return response

# Query parameters
@products_router.get(
  '/products/', 
  tags=tags, 
  response_model=List[ProductSchema], 
  status_code=200, 
  dependencies=[Depends(UserPermission('all'))]
)
def get_products_by_line(product_line: str = Query(max_length=30)):
  '''Get products by product line for all users'''
  db = SessionDB()
  products = (
    db.query(ProductLine)
    .filter(ProductLine.name == product_line)
    .first()
    .products
  )
  
  response = JSONResponse(content=products, status_code=200)
  if not products:
    response = JSONResponse(content={'message': 'Product line not found'}, status_code=404)
    
  return response

@products_router.post(
  '/products', 
  tags=tags, 
  response_model=dict, 
  status_code=201, 
  dependencies=[Depends(UserPermission('admin'))]
)
def add_product(product: CreateProductSchema):
  '''Add product for admin users'''
  db = SessionDB()
  new_product = Product(**product.model_dump())
  db.add(new_product)
  db.commit()
  return JSONResponse(content={'message': 'Product added successfully'}, status_code=201)

@products_router.put(
  '/products/{id}', 
  tags=tags, 
  response_model=dict, 
  status_code=200, 
  dependencies=[Depends(UserPermission('admin'))]
)
def update_product(id: int, product: CreateProductSchema):
  '''Update product by id for admin users'''
  db = SessionDB()
  product_query = db.query(Product).filter(Product.id == id).first()
  
  if not product_query:
    return JSONResponse(content={'message': 'Product not found'}, status_code=404)
  
  product_query.name = product.name
  product_query.price = product.price
  product_query.product_line_id = product.product_line_id
  
  db.commit()
    
  return JSONResponse(content={'message': 'Product updated successfully'}, status_code=200)

@products_router.delete('/products/{id}', tags=tags, response_model=dict, status_code=200, dependencies=[Depends(UserPermission('admin'))])
def delete_product(id: int):
  '''Delete product by id for admin users'''
  db = SessionDB()
  product = db.query(Product).filter(Product.id == id).first()
  if not product:
    return JSONResponse(content={'message': 'Product not found'}, status_code=404)
  
  db.delete(product)
  db.commit()
    
  return JSONResponse(content={'message': 'Product deleted successfully'}, status_code=200)