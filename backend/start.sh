#!/bin/bash

# タイムゾーン設定の確認（デバッグ用）
echo "現在のタイムゾーン設定: $(cat /etc/timezone)"
date

# cronデーモンを起動
service cron start
echo "cronデーモンを起動しました"

# cronジョブの確認（デバッグ用）
echo "設定されているcronジョブ:"
crontab -l

# FastAPIサーバーを起動
exec uvicorn src.api.main:app --host 0.0.0.0 --port 8000 