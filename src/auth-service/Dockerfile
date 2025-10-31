FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends --no-install-suggests \
      build-essential libpq-dev python3-dev \
      && pip install --no-cache-dir --upgrade pip \
      && pip install --no-cache-dir -r requirements.txt \
      && apt-get purge -y build-essential python3-dev \
      && apt-get autoremove -y \
      && rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 5000

ENV HOST=0.0.0.0
ENV PORT=5000
ENV APP_MODULE=main:app

CMD uvicorn $APP_MODULE --host $HOST --port $PORT
