from .database import SessionLocal
from . import models

def seed_data():
    db = SessionLocal()
    try:
        # 1. 建立預設賣家 (Lin Boyu)
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

        # 2. 建立 AirPods 4 貼文 (更換為 Web 友善圖片網址)
        existing_p = db.query(models.Product).filter(models.Product.id == 1).first()
        if not existing_p:
            new_p = models.Product(
                id=1,
                content="全新 AirPods 4，國北教大面交優先！這款音質真的推。",
                price=5000.0,
                # 這裡使用了 Unsplash 的開放 API 圖片，這張圖在 Web 渲染時不會有 CORS 紅線
                image_url="https://images.unsplash.com/photo-1603351154351-5e2d0600bb77?q=80&w=1000&auto=format&fit=crop",
                owner_id=1,
                commission_rate=0.05
            )
            db.add(new_p)
            db.commit()
            print("✅ AirPods 4 貼文播種成功 (已更新圖片來源)")
        else:
            # 如果資料已存在，強制更新圖片網址，確保紅線消失
            existing_p.image_url = "https://images.unsplash.com/photo-1603351154351-5e2d0600bb77?q=80&w=1000&auto=format&fit=crop"
            db.commit()
            print("✅ 已強制更新現有資料的圖片網址")
            
    except Exception as e:
        print(f"❌ Seed Error: {e}")
    finally:
        db.close()