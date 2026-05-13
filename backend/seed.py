from .database import SessionLocal
from . import models

def seed_data():
    db = SessionLocal()
    try:
        # 1. 建立預設賣家 (測試帳號)
        admin = db.query(models.User).filter(models.User.id == 1).first()
        if not admin:
            admin = models.User(
                id=1,
                username="林帛諭_Dev",
                avatar_url="https://api.dicebear.com/7.x/avataaars/svg?seed=Lin"
            )
            db.add(admin)
            db.commit()
            print("✅ 測試賣家帳號已建立")

        # 2. 建立 AirPods 4 商品並關聯到該賣家
        existing_product = db.query(models.Product).filter(models.Product.id == 1).first()
        if not existing_product:
            new_product = models.Product(
                id=1,
                content="全新 AirPods 4，國北教大面交優先！",
                price=5000.0,
                image_url="https://www.apple.com/v/airpods-4/a/images/overview/finish/finish_airpods_4__f9p4id59v96u_large.jpg",
                owner_id=1, # 關聯到剛剛建立的 User ID 1
                commission_rate=0.05
            )
            db.add(new_product)
            db.commit()
            print("✅ AirPods 4 播種成功，已掛載至賣家帳號")
        else:
            print("ℹ️ 資料已存在，跳過播種。")
            
    except Exception as e:
        print(f"❌ Seed Error: {e}")
    finally:
        db.close()