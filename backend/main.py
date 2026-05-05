from fastapi import FastAPI
from pydantic import BaseModel
# main.py
import os
from fastapi import FastAPI

app = FastAPI()
# ... 剩下的代碼

app = FastAPI()

# 模擬資料庫裡的商品資料
fake_db = {
    "product_001": {
        "name": "二手 AirPods 4 (降噪版)",
        "price": 3800,
        "seller": "lin_bo_yu",
        "desc": "來自 Threads 的精選商品，保存良好。"
    }
}

@app.get("/product/{pid}")
async def get_product(pid: str):
    if pid in fake_db:
        item = fake_db[pid]
        # 技術總監提醒：後端計算佣金最安全，防止前端被竄改
        commission = int(item["price"] * 0.05)
        return {
            "id": pid,
            "name": item["name"],
            "price": item["price"],
            "platform_fee": commission,
            "total_with_fee": item["price"] + commission,
            "seller": item["seller"],
            "description": item["desc"]
        }
    return {"error": "商品不存在"}

# 啟動指令：uvicorn main:app --reload