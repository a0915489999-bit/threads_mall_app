from sqlalchemy import Column, Integer, String, Float
from .database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    avatar_url = Column(String, default="https://via.placeholder.com/150")
    # 關聯：一個用戶可以發多個商品，留多個言
    products = relationship("Product", back_populates="owner")
    comments = relationship("Comment", back_populates="author")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)  # 像 Threads 的發文內容
    price = Column(Float)
    image_url = Column(String)
    commission_rate = Column(Float, default=0.05) # 5% 抽成
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="products")
    comments = relationship("Comment", back_populates="product")

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    product_id = Column(Integer, ForeignKey("products.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    product = relationship("Product", back_populates="comments")
    author = relationship("User", back_populates="comments")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    commission_rate = Column(Float, default=0.05) # 5% 佣金