# seed.py
from database import SessionLocal
import models

def seed_data():
    db = SessionLocal()
    try:
        # 關鍵：檢查 ID=1 是否存在
        product = db.query(models.Product).filter(models.Product.id == 1).first()
        if not product:
            print("Creating seed data...")
            new_p = models.Product(
                id=1,
                name="二手 AirPods 4 (降噪版)",
                price=3800.0,
                commission_rate=0.05
            )
            db.add(new_p)
            db.commit()
            print("✅ Seed success!")
        else:
            print("Product already exists.")
    except Exception as e:
        print(f"❌ Seed error: {e}")
    finally:
        db.close()