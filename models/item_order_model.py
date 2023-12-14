from config.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

class ItemOrder(Base):
  __tablename__ = 'items_orders'
  
  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))
  product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
  quantity: Mapped[int] = mapped_column(nullable=False)
  
  order = relationship(
    'Order', 
    back_populates='items', 
    uselist=False, 
    cascade='all'
  )
  
  product = relationship(
    'Product', 
    back_populates='items_orders', 
    uselist=False, 
    cascade='all'
  )
  
  