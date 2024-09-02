# 使用官方 Python 運行時作為父鏡像
FROM python:3.12.4-slim

# 設置工作目錄
WORKDIR /app

# 將當前目錄內容複製到容器中的 /app
COPY . /app

# 安裝依賴
RUN pip install --no-cache-dir -r requirements.txt

# 創建日誌目錄
RUN mkdir -p /app/logs

# 設置環境變量
ENV LOG_DIR=/app/logs

# 暴露日誌目錄為卷
VOLUME /app/logs

# 運行應用
CMD ["python", "course_query_system.py"]