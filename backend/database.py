import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 取得環境變數
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# --- 診斷代碼：這會在 Render 日誌顯示連線狀況 ---
if SQLALCHEMY_DATABASE_URL:
    print(f"📡 [DEBUG] 正在連線至資料庫，網址開頭為: {SQLALCHEMY_DATABASE_URL[:10]}...")
else:
    print("❌ [ERROR] 完全讀取不到 DATABASE_URL 環境變數！")
# --------------------------------------------

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()