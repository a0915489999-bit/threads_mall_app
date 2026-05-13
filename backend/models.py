from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    avatar_url = Column(String)
    products = relationship("Product", back_populates="owner")

class Product(Base):
    __tablename__ = "products"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    price = Column(Float)
    image_url = Column(String)
    commission_rate = Column(Float, default=0.05)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="products")
    # 新增：與留言的關聯
    comments = relationship("Comment", back_populates="product", cascade="all, delete-orphan")

class Comment(Base):
    __tablename__ = "comments"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    user_name = Column(String) # 留言者的名稱
    created_at = Column(DateTime, default=datetime.utcnow)
    
    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product", back_populates="comments")