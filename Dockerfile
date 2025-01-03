FROM python:3.9

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 腳本
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# 複製專案檔案
COPY . /app/

ENTRYPOINT ["./entrypoint.sh"]