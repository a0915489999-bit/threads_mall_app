from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import os

# 這裡使用相對路徑導入
from . import models, seed
from .database import engine, get_db

app = FastAPI()
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # <--- 1. 加入這行
from sqlalchemy.orm import Session
import os
from . import models, seed
from .database import engine, get_db

app = FastAPI()

# 2. 加入 CORS 設定，允許你的 Flutter Web 抓資料
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允許所有來源
    allow_credentials=True,
    allow_methods=["*"],  # 允許所有方法 (GET, POST 等)
    allow_headers=["*"],  # 允許所有標頭
)

# ... 下面的程式碼保持不變 ...

# 伺服器啟動時自動執行的任務
@app.on_event("startup")
def startup_event():
    print("🚀 正在啟動伺服器並檢查資料庫...")
    try:
        # 1. 自動建立所有資料表 (如果不存在的話)
        models.Base.metadata.create_all(bind=engine)
        
        # 2. 自動執行播種腳本，塞入 AirPods 4 資料
        seed.seed_data()
        print("✅ 資料庫初始化與播種完成！")
    except Exception as e:
        print(f"❌ 啟動初始化失敗: {e}")

# 根路徑測試
@app.get("/")
def read_root():
    return {
        "status": "Online",
        "database": "PostgreSQL Connected",
        "message": "歡迎來到 Threads Mall API"
    }

# 取得商品詳細資料的 API
@app.get("/product/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        # 如果還是找不到，嘗試在查詢前再播種一次 (這是雙重保險)
        seed.seed_data()
        product = db.query(models.Product).filter(models.Product.id == product_id).first()
        
        if not product:
            raise HTTPException(status_code=404, detail="商品不存在於資料庫中")
    
    return product