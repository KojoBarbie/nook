FROM python:3.10-slim

WORKDIR /app

# cronとタイムゾーン設定用パッケージのインストール
RUN apt-get update && apt-get install -y cron tzdata && rm -rf /var/lib/apt/lists/*
# タイムゾーンを日本時間に設定
RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime
RUN echo "Asia/Tokyo" > /etc/timezone

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV PYTHONPATH=/app

# cronジョブの設定（毎日朝9時に実行）
RUN echo "0 9 * * * cd /app && python -m src.services.run_services --service all >> /var/log/cron.log 2>&1" > /etc/cron.d/nook-cron
RUN chmod 0644 /etc/cron.d/nook-cron
RUN crontab /etc/cron.d/nook-cron
RUN touch /var/log/cron.log

# スタートアップスクリプトの作成
COPY ./start.sh /start.sh
RUN chmod +x /start.sh
CMD ["/start.sh"]
