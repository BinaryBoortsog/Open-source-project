FROM python:3.12-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY tor-crawler /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["bash", "-c", "python -u crawler_runner.py 2>&1 & uvicorn web.app:app --host 0.0.0.0 --port 8000"]
