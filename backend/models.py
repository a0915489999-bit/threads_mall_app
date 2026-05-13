from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    avatar_url = Column(String, default="https://api.dicebear.com/7.x/avataaars/svg?seed=Lin")
    
    products = relationship("Product", back_populates="owner")

class Product(Base):
    __tablename__ = "products"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    price = Column(Float)
    image_url = Column(String)
    commission_rate = Column(Float, default=0.05) # 5% 佣金
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="products")