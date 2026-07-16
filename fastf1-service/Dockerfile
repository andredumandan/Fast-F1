# fastf1-service/Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY fastf1-service ./fastf1-service
EXPOSE 8000
ENV PORT=8000
# Use shell form so $PORT is expanded at runtime
CMD uvicorn fastf1-service.main:app --host 0.0.0.0 --port $PORT
