

import datetime

from config.database import Base, engine, SessionDB

from models.item_order_model import *
from models.order_model import *
from models.user_model import *
from models.product_model import *

from utils.hashing import hash_password


def seed():
  Base.metadata.create_all(engine)

  db = SessionDB()
  
  password_users = hash_password('12345678')

  # Create users
  admin = UserAdmin(
    email='admin@mail.com',
    password=password_users
  )
  client1 = UserClient(
    email='client1@mail.com',
    password=password_users
  )
  client2 = UserClient(
    email='client2@mail.com',
    password=password_users
  )
  delivery = UserDelivery(
    email='delivery@mail.com',
    password=password_users
  )
  db.add_all([admin, client1, client2, delivery])
  
  
  # Create product lines
  product_lines = [
    ProductLine(name='Bebidas'),
    ProductLine(name='Postres'),
    ProductLine(name='Platos fuertes'),
    ProductLine(name='Entradas'),
  ]
  db.add_all(product_lines)
  
  # Create products
  products = [
    Product(
      name='Coca cola',
      price=2000,
      product_line=product_lines[0]
    ),
    Product(
      name='Pepsi',
      price=2000,
      product_line=product_lines[0]
    ),
    Product(
      name='Tres leches',
      price=5000,
      product_line=product_lines[1]
    ),
    Product(
      name='Flan',
      price=5000,
      product_line=product_lines[1]
    ),
    Product(
      name='Carne asada de cerdo',
      price=14000,
      product_line=product_lines[2]
    ),
    Product(
      name='Pollo asado',
      price=8000,
      product_line=product_lines[2]
    ),
    Product(
      name='Patacones',
      price=5000,
      product_line=product_lines[3]
    ),
    Product(
      name='Empanadas',
      price=3000,
      product_line=product_lines[3]
    ),
  ]
  db.add_all(products)
  
  
  # Create order items
  items_orders = [
    ItemOrder(
      quantity=2,
      product=products[0]
    ),
    ItemOrder(
      quantity=1,
      product=products[2]
    ),
    ItemOrder(
      quantity=1,
      product=products[4]
    ),
    ItemOrder(
      quantity=3,
      product=products[6]
    ),
  ]
  db.add_all(items_orders)
  
  
  # Create orders
  orders = [
    Order(
      client=client1,
      delivery=delivery,
      date=datetime.datetime.now(),
      items=items_orders[:2],
      total=sum(map(lambda item: item.quantity*item.product.price, items_orders[:2])),
      state=StatesOrder.pending
    ),
    Order(
      client=client2,
      delivery=delivery,
      date=datetime.datetime.now(),
      items=items_orders[2:4],
      total=sum(list(map(lambda item: item.quantity*item.product.price, items_orders[2:4]))),
      state=StatesOrder.pending
    ),
  ]
  db.add_all(orders)
  
  
  db.commit()
  db.close()
  
  
if __name__ == '__main__':
  seed()
  
