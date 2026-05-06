from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, database, seed # 確保有 import seed.py
from database import engine, get_db

# 1. 啟動時自動建立表格結構
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 2. 核心修復：伺服器啟動時，自動執行一次 seed.py
@app.on_event("startup")
def startup_event():
    print("🚀 伺服器啟動中：正在執行資料庫初始化...")
    seed.seed_data() # 這會呼叫你 seed.py 裡的函數