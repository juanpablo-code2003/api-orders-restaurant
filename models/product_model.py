from config.database import Base
from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column

class Product(Base):
  __tablename__ = 'products'
  
  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
  price: Mapped[int] = mapped_column(nullable=False)
  
  items_orders = relationship(
    'ItemOrder', 
    back_populates='product', 
    cascade='all'
  )