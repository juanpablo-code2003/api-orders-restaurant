from config.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

class ItemOrder(Base):
  __tablename__ = 'items_orders'
  
  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  order_id: Mapped[int] = mapped_column(ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
  product_id: Mapped[int] = mapped_column(ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
  quantity: Mapped[int] = mapped_column(nullable=False)
  
  order = relationship(
    'Order', 
    back_populates='items', 
    uselist=False
  )
  
  product = relationship(
    'Product', 
    back_populates='items_orders', 
    uselist=False
  )
  
  