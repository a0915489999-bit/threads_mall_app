from .database import SessionLocal
from . import models  # 關鍵：這樣才能用 models.Product

def seed_data():
    db = SessionLocal()
    try:
        # 確保 models.Product 已經被正確定義且對應到資料表
        # 檢查是否已經有 AirPods 4 (ID 為 1)
        existing_product = db.query(models.Product).filter(models.Product.id == 1).first()
        
        if not existing_product:
            print("正在寫入 AirPods 4 到資料庫...")
            new_product = models.Product(
                id=1,
                name="AirPods 4",
                price=5000,
                commission_rate=0.05
            )
            db.add(new_product)
            db.commit()
            print("✅ 種子資料寫入成功！")
        else:
            print("ℹ️ 資料已存在，跳過初始化。")
    except Exception as e:
        # 這裡就是你剛才看到 "name 'models' is not defined" 的地方
        print(f"❌ Seed error: {e}")
    finally:
        db.close()