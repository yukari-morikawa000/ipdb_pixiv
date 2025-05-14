FROM python:3.12-slim

WORKDIR /app

# 依存ライブラリのインストール（Playwrightに必要な依存含む）
RUN apt-get update && apt-get install -y \
    wget \
    libnss3 \
    libatk-bridge2.0-0 \
    libxss1 \
    libgtk-3-0 \
    libasound2 \
    libgbm1 \
    libxshmfence1 \
    libxcomposite1 \
    libxrandr2 \
    libpangocairo-1.0-0 \
    libpangoft2-1.0-0 \
    libcups2 \
    libdrm2 \
    fonts-noto-color-emoji \
    && apt-get clean

# Python依存ライブラリのインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Playwrightブラウザのインストール（ここが重要！）
RUN playwright install --with-deps

COPY . .

CMD ["python", "search_pixiv.py"]
