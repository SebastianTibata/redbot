FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app
COPY wait-for-db.sh /wait-for-db.sh
RUN apt-get update && apt-get install -y netcat-openbsd && chmod +x /wait-for-db.sh

CMD ["/wait-for-db.sh", "db", "5432", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
