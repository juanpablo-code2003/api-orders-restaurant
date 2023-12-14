from config.database import Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

class Product(Base):
  __tablename__ = 'products'
  
  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
  price: Mapped[int] = mapped_column(nullable=False)
  product_line_id: Mapped[int] = mapped_column(ForeignKey('product_lines.id'), nullable=False)
  
  items_orders = relationship(
    'ItemOrder', 
    back_populates='product', 
    cascade='all'
  )
  
  product_line = relationship(
    'ProductLine', 
    back_populates='products', 
    uselist=False,
    cascade='all'
  )
  

class ProductLine(Base):
  __tablename__ = 'product_lines'
  
  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
  
  products = relationship(
    'Product', 
    back_populates='product_line', 
    cascade='all'
  )