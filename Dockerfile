FROM python:3.10

# 設定工作目錄為 /app
WORKDIR /app

# Python 環境變數設定
# 防止 Python 產生 .pyc 檔案
ENV PYTHONDONTWRITEBYTECODE 1

# 防止 Python 緩衝輸出，確保日誌即時顯示
ENV PYTHONUNBUFFERED 1

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 複製 requirements.txt 到工作目錄
COPY requirements.txt /app/

# 安裝 Python 套件，--no-cache-dir 可以減少映像大小
RUN pip install --no-cache-dir -r requirements.txt

# 複製當前目錄下的所有檔案到容器的工作目錄
COPY . .

# 給予 entrypoint.sh 執行權限
RUN chmod +x entrypoint.sh

# 執行腳本
ENTRYPOINT ["bash", "./entrypoint.sh"]