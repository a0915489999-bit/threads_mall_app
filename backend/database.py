import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 從環境變數讀取網址，如果沒有則使用本地測試用的路徑
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# 建立資料庫引擎
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 獲取資料庫連線的工具函數
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()