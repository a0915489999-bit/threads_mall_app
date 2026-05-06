from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import engine, get_db
import seed  # 確保導入你的 seed.py

# 啟動時自動建立 PostgreSQL 資料表結構
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 核心功能：伺服器啟動時自動執行種子資料寫入
@app.on_event("startup")
def startup_event():
    print("🚀 伺服器啟動中：正在執行資料庫初始化...")
    seed.seed_data()

# 根目錄：測試連線是否正常
@app.get("/")
def read_root():
    return {
        "status": "Online",
        "database": "PostgreSQL Connected",
        "message": "Welcome to Threads Mall API"
    }

# 正式的商品查詢介面：直接對接資料庫
@app.get("/product/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    # 從資料庫搜尋對應 ID 的商品
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在於資料庫中")
    
    # 由後端統一計算佣金，確保安全性
    commission = int(product.price * product.commission_rate)
    
    return {
        "id": f"product_{product.id:03d}", # 格式化為 product_001
        "name": product.name,
        "price": product.price,
        "platform_fee": commission,
        "total_with_fee": product.price + commission,
        "description": "來自 Threads 的精選商品，保存良好。"
    }