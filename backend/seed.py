from .database import SessionLocal
from . import models

def seed_data():
    db = SessionLocal()
    try:
        # 1. 建立預設賣家
        admin = db.query(models.User).filter(models.User.id == 1).first()
        if not admin:
            admin = models.User(
                id=1,
                username="林帛諭_Developer",
                avatar_url="https://api.dicebear.com/7.x/avataaars/svg?seed=Lin"
            )
            db.add(admin)
            db.commit()
            print("✅ 測試賣家帳號已建立")

        # 2. 建立 AirPods 4 貼文
        existing_p = db.query(models.Product).filter(models.Product.id == 1).first()
        if not existing_p:
            new_p = models.Product(
                id=1,
                content="全新 AirPods 4，國北教大面交優先！這款音質真的推。",
                price=5000.0,
                image_url="https://www.apple.com/v/airpods-4/a/images/overview/finish/finish_airpods_4__f9p4id59v96u_large.jpg",
                owner_id=1,
                commission_rate=0.05
            )
            db.add(new_p)
            db.commit()
            print("✅ AirPods 4 貼文播種成功")
            
    except Exception as e:
        print(f"❌ Seed Error: {e}")
    finally:
        db.close()