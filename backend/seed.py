from database import SessionLocal
import models

def seed_data():
    db = SessionLocal()
    
    # 檢查是否已經有資料，避免重複插入
    existing_product = db.query(models.Product).filter(models.Product.id == 1).first()
    
    if not existing_product:
        test_product = models.Product(
            id=1,
            name="Threads 聯名限量 T-Shirt",
            price=590.0,
            commission_rate=0.05
        )
        db.add(test_product)
        db.commit()
        print("✅ 成功寫入第一筆種子商品資料！")
    else:
        print("ℹ️ 資料庫中已存在商品資料，跳過寫入。")
    
    db.close()

if __name__ == "__main__":
    seed_data()