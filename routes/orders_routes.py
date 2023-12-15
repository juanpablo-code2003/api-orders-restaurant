import random
import datetime

from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List

from middlewares.permission_user import UserPermission
from config.database import SessionDB
from models.user_model import User, UserDelivery, roles_user
from models.order_model import Order, StatesOrder
from models.item_order_model import ItemOrder
from models.product_model import Product
from schemas.order_schemas import OrderSchema, CreateOrderSchema, UpdateStateOrderSchema


orders_router = APIRouter()

tags = ['Orders']

@orders_router.get(
  '/orders', 
  tags=tags, 
  response_model=List[OrderSchema], 
  status_code=200
)
def get_all_orders(current_user: User = Depends(UserPermission('all'))) -> List[OrderSchema]:
  '''Get all orders with user role'''
  db = SessionDB()
  orders = db.query(Order)
  if isinstance(current_user, roles_user.get('client')):
    orders = orders.filter(Order.client_id == current_user.id)
  elif isinstance(current_user, roles_user.get('delivery')):
    orders = orders.filter(Order.delivery_id == current_user.id)
    
  orders = orders.all()
  for order in orders:
    db.refresh(order, ['items'])
  return JSONResponse(content=jsonable_encoder(orders), status_code=200)

@orders_router.get(
  '/orders/{id}', 
  tags=tags, 
  response_model=OrderSchema, 
  status_code=200
)
def get_order_by_id(id: int, current_user: User = Depends(UserPermission('all'))):
  '''Get order by id with user role'''
  db = SessionDB()
  order = db.query(Order).filter(Order.id == id)
  if current_user.role == 'client':
    order = order.filter(Order.client_id == current_user.id)
  elif current_user.role == 'delivery':
    order = order.filter(Order.delivery_id == current_user.id)
    
  order = order.first()
  if order:
    db.refresh(order, ['items'])
  
  
  response = JSONResponse(content=jsonable_encoder(order), status_code=200)
  if not order:
    response = JSONResponse(content={'message': 'Order not found'}, status_code=404)
    
  return response

# Query parameters
@orders_router.get(
  '/orders/', 
  tags=tags, 
  response_model=List[OrderSchema], 
  status_code=200
)
def get_orders_by_state(state: str, current_user: User = Depends(UserPermission('all'))):
  '''Get orders by state with user role'''
  db = SessionDB()
  orders = (
    db.query(Order)
    .filter(Order.state == state)
  )
  
  if current_user.role == 'client':
    orders = orders.filter(Order.client_id == current_user.id)
  elif current_user.role == 'delivery':
    orders = orders.filter(Order.delivery_id == current_user.id)
    
  orders = orders.all()
  
  response = JSONResponse(content=orders, status_code=200)
  if not orders:
    response = JSONResponse(content={'message': 'Order line not found'}, status_code=404)
    
  return response

@orders_router.post(
  '/orders', 
  tags=tags, 
  response_model=dict, 
  status_code=201
)
def add_order(order: CreateOrderSchema, current_user: User = Depends(UserPermission('client'))):
  '''Add order for client users'''
  db = SessionDB()
  available_deliveries = db.query(UserDelivery).all()
  if not available_deliveries:
    return JSONResponse(
      content={'message': 'Available deliveries for new order not found'}, 
      status_code=404
    )
    
  new_items_order = list(map(lambda item: ItemOrder(**item.model_dump()), order.items))
  
  for it in new_items_order:
    product = db.query(Product).filter(Product.id == it.product_id).first()
    it.product = product
    
  new_order = Order(
    client_id=current_user.id,
    delivery_id=random.choice(available_deliveries).id,
    date=datetime.datetime.now(),
    total=sum(map(lambda item: item.quantity*item.product.price, new_items_order)),
    state=StatesOrder.pending
  )
  
  for it in new_items_order:
    it.order = new_order
  
  new_order.items = new_items_order
  
  db.add(new_order)
  db.commit()
  return JSONResponse(content={'message': 'Order added successfully'}, status_code=201)

@orders_router.put(
  '/orders/{id}', 
  tags=tags, 
  response_model=dict, 
  status_code=200
)
def update_items_order(id: int, order: CreateOrderSchema, current_user: User = Depends(UserPermission('client'))):
  '''Update items order for client users'''
  db = SessionDB()
  order_query = db.query(Order).filter(Order.id == id, Order.client_id == current_user.id).first()
  
  response = None
  
  if not order_query:
    response = JSONResponse(content={'message': 'Order not found'}, status_code=404)
  
  if order_query.state != StatesOrder.pending:
    response = JSONResponse(content={'message': 'Order is not pending'}, status_code=400)
    
  if response is not None:
    return response
  
  previous_items_order = order_query.items
  for prev_it in previous_items_order:
    db.delete(prev_it)
  
  new_items_order = list(map(lambda item: ItemOrder(**item.model_dump()), order.items))
  
  for it in new_items_order:
    product = db.query(Product).filter(Product.id == it.product_id).first()
    it.product = product
    
  order_query.items = new_items_order
  
  db.commit()

  return JSONResponse(content={'message': 'Order updated successfully'}, status_code=200)


@orders_router.put(
  '/orders/{id}/state', 
  tags=tags, 
  response_model=dict, 
  status_code=200
)
def update_state_order(id: int, order_state: UpdateStateOrderSchema, current_user: User = Depends(UserPermission('delivery', 'admin'))):
  '''Update state order for delivery and admin users'''
  db = SessionDB()
  order = db.query(Order).filter(Order.id == id).first()
  
  if not order:
    return JSONResponse(content={'message': 'Order not found'}, status_code=404)
  
  if current_user.role == 'delivery' and order.delivery_id != current_user.id:
    return JSONResponse(content={'message': 'Order is not assigned to this delivery'}, status_code=400)
  
  order.state = order_state.state
  
  db.commit()
    
  return JSONResponse(content={'message': 'Order updated successfully'}, status_code=200)


@orders_router.delete(
  '/orders/{id}', 
  tags=tags, 
  response_model=dict, 
  status_code=200
)
def cancel_order(id: int, current_user: User = Depends(UserPermission('client'))):
  '''Cancel order for client users'''
  db = SessionDB()
  order = db.query(Order).filter(Order.id == id, Order.client_id == current_user.id).first()
  
  if not order:
    return JSONResponse(content={'message': 'Order not found'}, status_code=404)
  
  order.state = StatesOrder.canceled
  
  db.commit()
    
  return JSONResponse(content={'message': 'Order cancelled successfully'}, status_code=200)