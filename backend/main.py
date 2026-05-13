from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from . import models, seed
from .database import engine, get_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProductCreate(BaseModel):
    content: str
    price: float
    image_url: str
    username: str # 前端傳入目前使用者名稱

class CommentCreate(BaseModel):
    product_id: int
    content: str
    username: str

@app.on_event("startup")
def startup_event():
    models.Base.metadata.create_all(bind=engine)
    seed.seed_data()

@app.get("/feed/")
def get_feed(db: Session = Depends(get_db)):
    products = db.query(models.Product).order_by(models.Product.created_at.desc()).all()
    return [{
        "id": p.id,
        "username": p.owner.username if p.owner else "匿名賣家",
        "avatar_url": p.owner.avatar_url if p.owner else "https://api.dicebear.com/7.x/avataaars/svg?seed=Guest",
        "content": p.content,
        "price": p.price,
        "image_url": p.image_url,
        "comments_count": len(p.comments)
    } for p in products]

@app.post("/products/")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    # 查找或建立用戶
    user = db.query(models.User).filter(models.User.username == product.username).first()
    if not user:
        user = models.User(username=product.username, avatar_url=f"https://api.dicebear.com/7.x/avataaars/svg?seed={product.username}")
        db.add(user)
        db.commit()
        db.refresh(user)
    
    new_prod = models.Product(content=product.content, price=product.price, image_url=product.image_url, owner_id=user.id)
    db.add(new_prod)
    db.commit()
    return {"status": "success"}

@app.post("/comments/")
def add_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    new_comment = models.Comment(product_id=comment.product_id, content=comment.content, user_name=comment.username)
    db.add(new_comment)
    db.commit()
    return {"status": "success"}

@app.get("/comments/{product_id}")
def get_comments(product_id: int, db: Session = Depends(get_db)):
    return db.query(models.Comment).filter(models.Comment.product_id == product_id).all()