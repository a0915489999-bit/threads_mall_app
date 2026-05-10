from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

# 🔴 關鍵修正：加上 "." 代表在「同一個資料夾」內尋找
from . import models, seed
from .database import engine, get_db

# ... 後面的程式碼保持不變

# 啟動時自動建立資料庫表結構
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 核心：伺服器啟動時自動檢查並寫入 AirPods 種子資料
@app.on_event("startup")
def startup_event():
    print("🚀 伺服器啟動：執行資料庫初始化...")
    seed.seed_data()

# 根目錄：用來檢查 API 是否活著
@app.get("/")
def read_root():
    return {
        "status": "Online",
        "database": "PostgreSQL Connected",
        "message": "歡迎來到 Threads Mall API"
    }

# 商品查詢介面：直接對接 PostgreSQL
@app.get("/product/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    # 搜尋 ID 為 1 的商品
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在於資料庫中")
    
    # 後端計算 5% 佣金
    commission = int(product.price * product.commission_rate)
    
    return {
        "id": product.id,
        "name": product.name,
        "price": int(product.price),
        "platform_fee": commission,
        "total_with_fee": int(product.price + commission),
        "seller": "lin_bo_yu",
        "description": "來自 Threads 的精選商品，保存良好，附原廠盒裝。國北教大校園可面交。"
    }