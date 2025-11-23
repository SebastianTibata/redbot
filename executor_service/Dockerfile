FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN apt-get update && apt-get install -y dos2unix netcat-openbsd
RUN dos2unix /app/wait-for-db.sh && chmod +x /app/wait-for-db.sh
CMD ["/app/wait-for-db.sh", "db", "5432", "python", "-m", "app.executor.worker"]