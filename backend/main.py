from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import os

from . import models, seed
from .database import engine, get_db

app = FastAPI()

# 開放 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 定義前端發送過來的資料格式
class ProductCreate(BaseModel):
    content: str
    price: float
    image_url: str
    owner_id: int

@app.on_event("startup")
def startup_event():
    print("🚀 啟動中...")
    try:
        # 注意：這裡已經移除 drop_all，以免每次啟動都清空你的資料
        models.Base.metadata.create_all(bind=engine)
        seed.seed_data()
    except Exception as e:
        print(f"❌ 啟動失敗: {e}")

@app.get("/")
def read_root():
    return {"status": "Online", "version": "v2.0-social"}

# 取得動態牆 (Feed)
@app.get("/feed/")
def get_feed(db: Session = Depends(get_db)):
    products = db.query(models.Product).order_by(models.Product.created_at.desc()).all()
    result = []
    for p in products:
        result.append({
            "id": p.id,
            "username": p.owner.username if p.owner else "未知用戶",
            "avatar_url": p.owner.avatar_url if p.owner else "",
            "content": p.content,
            "price": p.price,
            "image_url": p.image_url,
            "commission_rate": p.commission_rate
        })
    return result

# 新增商品 (發文上架)
@app.post("/products/")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = models.Product(
        content=product.content,
        price=product.price,
        image_url=product.image_url,
        owner_id=product.owner_id,
        commission_rate=0.05
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product