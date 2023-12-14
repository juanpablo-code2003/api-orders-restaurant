from config.database import Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

class User(Base):
  __tablename__ = 'users'
  
  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
  password: Mapped[str] = mapped_column(String(50), nullable=False)
  role: Mapped[str] = mapped_column(nullable=False)
  
  __mapper_args__ = {
    'polymorphic_identity': 'user',
    'polymorphic_on': 'role'
  }
  

class UserAdmin(User):
  __tablename__ = 'admins'
  
  id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
  
  __mapper_args__ = {
    'polymorphic_identity': 'admin'
  }
  
class UserClient(User):
  __tablename__ = 'clients'
  
  id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
  
  orders = relationship(
    'Order', 
    back_populates='client', 
    cascade='all, delete-orphan'
  )
  
  __mapper_args__ = {
    'polymorphic_identity': 'client'
  }
  
class UserDelivery(User):
  __tablename__ = 'deliveries'
  
  id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
  
  orders = relationship(
    'Order', 
    back_populates='delivery', 
    cascade='all, delete-orphan'
  )
  
  __mapper_args__ = {
    'polymorphic_identity': 'delivery'
  }
  
  
roles_user = {
  'admin': UserAdmin,
  'client': UserClient,
  'delivery': UserDelivery
}
  
  