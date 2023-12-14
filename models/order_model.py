import enum

from config.database import Base
from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

class States(enum.Enum):
  pending = 'pending'
  delivered = 'delivered'
  canceled = 'canceled'

class Order(Base):
  __tablename__ = 'orders'
  
  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  client_id: Mapped[int] = mapped_column(ForeignKey('clients.id'))
  delivery_id: Mapped[int] = mapped_column(ForeignKey('deliveries.id'))
  date: Mapped[str] = mapped_column(nullable=False)
  total: Mapped[int] = mapped_column(nullable=False)
  state: Mapped[str] = mapped_column(Enum(States), nullable=False)
  
  
  client = relationship(
    'UserClient', 
    back_populates='orders', 
    uselist=False,
    cascade='all'
  )
  
  delivery = relationship(
    'UserDelivery', 
    back_populates='orders', 
    uselist=False,
    cascade='all'
  )
  
  items = relationship(
    'ItemOrder', 
    back_populates='order', 
    cascade='all, delete-orphan'
  )
  
  