import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. 讀取連線網址
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# 2. 自動修正連線字串 (解決 NoSuchModuleError)
if SQLALCHEMY_DATABASE_URL:
    # 如果是舊版的 postgres:// 則改為 postgresql://
    if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 3. 建立連線引擎
if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("❌ 錯誤：找不到 DATABASE_URL 環境變數，請在 Render 後台設定！")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()