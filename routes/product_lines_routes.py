from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List

from middlewares.permission_user import UserPermission
from config.database import SessionDB
from models.product_model import ProductLine
from schemas.product_schemas import ProductLineSchema, CreateProductLineSchema


product_lines_router = APIRouter()

tags = ['Products']

@product_lines_router.get(
  '/product_lines', 
  tags=tags, 
  response_model=List[ProductLineSchema], 
  status_code=200, 
  dependencies=[Depends(UserPermission('all'))]
)
def get_all_product_lines() -> List[ProductLineSchema]:
  db = SessionDB()
  product_lines = db.query(ProductLine).all()
  return JSONResponse(content=jsonable_encoder(product_lines), status_code=200)

@product_lines_router.get(
  '/product_lines/{id}', 
  tags=tags, 
  response_model=ProductLineSchema, 
  status_code=200, 
  dependencies=[Depends(UserPermission('all'))]
)
def get_product_by_id(id: int):
  db = SessionDB()
  product = db.query(ProductLine).filter(ProductLine.id == id).first()
  response = JSONResponse(content=jsonable_encoder(product), status_code=200)
  if not product:
    response = JSONResponse(content={'message': 'Product not found'}, status_code=404)
    
  return response

# Query parameters
@product_lines_router.get(
  '/product_lines/', 
  tags=tags, 
  response_model=List[ProductLineSchema], 
  status_code=200, 
  dependencies=[Depends(UserPermission('all'))]
)
def get_product_lines_by_name(name: str = Query(max_length=30)):
  db = SessionDB()
  product_lines = (
    db.query(ProductLine)
    .filter(ProductLine.name == name)
    .all()
  )
  
  response = JSONResponse(content=product_lines, status_code=200)
  if not product_lines:
    response = JSONResponse(content={'message': 'Product line not found'}, status_code=404)
    
  return response

@product_lines_router.post(
  '/product_lines', 
  tags=tags, 
  response_model=dict, 
  status_code=201, 
  dependencies=[Depends(UserPermission('admin'))]
)
def add_product_line(product_line: CreateProductLineSchema):
  db = SessionDB()
  new_product_line = ProductLine(**product_line.model_dump())
  db.add(new_product_line)
  db.commit()
  return JSONResponse(content={'message': 'Product line added successfully'}, status_code=201)

@product_lines_router.put(
  '/product_lines/{id}', 
  tags=tags, 
  response_model=dict, 
  status_code=200, 
  dependencies=[Depends(UserPermission('admin'))]
)
def update_product_line(id: int, product_line: CreateProductLineSchema):
  db = SessionDB()
  product_line_query = db.query(ProductLine).filter(ProductLine.id == id).first()
  
  if not product_line_query:
    return JSONResponse(content={'message': 'Product line not found'}, status_code=404)
  
  product_line_query.name = product_line.name
  
  db.commit()
    
  return JSONResponse(content={'message': 'Product line updated successfully'}, status_code=200)

@product_lines_router.delete('/product_lines/{id}', tags=tags, response_model=dict, status_code=200, dependencies=[Depends(UserPermission('admin'))])
def delete_product_line(id: int):
  db = SessionDB()
  product_line = db.query(ProductLine).filter(ProductLine.id == id).first()
  if not product_line:
    return JSONResponse(content={'message': 'Product line not found'}, status_code=404)
  
  db.delete(product_line)
  db.commit()
    
  return JSONResponse(content={'message': 'Product line deleted successfully'}, status_code=200)