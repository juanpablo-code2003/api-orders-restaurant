import enum

from config.database import Base
from sqlalchemy import ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column

class StatesOrder(enum.Enum):
  pending = 'pending'
  delivered = 'delivered'
  canceled = 'canceled'

class Order(Base):
  __tablename__ = 'orders'
  
  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  client_id: Mapped[int] = mapped_column(ForeignKey('clients.id', ondelete='CASCADE'), nullable=False)
  delivery_id: Mapped[int] = mapped_column(ForeignKey('deliveries.id', ondelete='CASCADE'), nullable=False)
  date: Mapped[str] = mapped_column(DateTime, nullable=False)
  total: Mapped[int] = mapped_column(nullable=False)
  state: Mapped[str] = mapped_column(Enum(StatesOrder), nullable=False)
  
  
  client = relationship(
    'UserClient', 
    back_populates='orders', 
    uselist=False
  )
  
  delivery = relationship(
    'UserDelivery', 
    back_populates='orders', 
    uselist=False
  )
  
  items = relationship(
    'ItemOrder', 
    back_populates='order'
  )
  
  