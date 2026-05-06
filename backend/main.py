from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import engine, get_db

# 啟動時自動建立資料庫表
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 根目錄路由，防止訪問時出現 404
@app.get("/")
def read_root():
    return {"status": "success", "message": "Threads Mall API is Online", "database": "Connected"}

# 正式的商品查詢路徑
@app.get("/product/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    # 從 PostgreSQL 資料庫搜尋
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在於資料庫中")
    
    # 計算佣金邏輯 (由後端統一控管)
    commission = int(product.price * product.commission_rate)
    
    return {
        "id": f"product_{product.id:03d}", # 格式化成你想要的 product_001 樣式
        "name": product.name,
        "price": product.price,
        "platform_fee": commission,
        "total_with_fee": product.price + commission,
        "description": "來自 Threads 的精選商品，保存良好。"
    }