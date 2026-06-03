FROM python:3.12-slim

RUN apt-get update \
  && apt-get install -y --no-install-recommends python3-tk tk \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir pymongo==4.8.0

COPY app ./app

CMD ["python", "-m", "app.main"]
