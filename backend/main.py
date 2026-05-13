from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os

from . import models, seed
from .database import engine, get_db

app = FastAPI()

# 開放 CORS 權限
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    print("🚀 正在執行資料庫強力重置與初始化...")
    try:
        # 1. 強力拆除舊結構 (解決重複定義報錯)
        models.Base.metadata.drop_all(bind=engine)
        
        # 2. 建立全新社交電商結構
        models.Base.metadata.create_all(bind=engine)
        
        # 3. 執行新版播種邏輯
        seed.seed_data()
        print("✅ 資料庫重生完成！")
    except Exception as e:
        print(f"❌ 啟動失敗: {e}")

@app.get("/")
def read_root():
    return {"status": "Online", "message": "Threads Mall API (Social Version) is running"}

# 取得動態牆 (Feed)
@app.get("/feed/")
def get_feed(db: Session = Depends(get_db)):
    # 這裡會回傳所有商品，包含賣家資訊
    products = db.query(models.Product).all()
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

@app.get("/product/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product