#!/usr/bin/env bash
# 出錯就停止執行
set -o errexit

# 安裝依賴
pip install --upgrade pip
pip install -r requirements.txt