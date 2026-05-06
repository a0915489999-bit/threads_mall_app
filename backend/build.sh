#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

# 執行種子資料腳本 (這行是新加的)
python seed.py