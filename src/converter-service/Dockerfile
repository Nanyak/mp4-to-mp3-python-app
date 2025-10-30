FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends --no-install-suggests \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*
COPY . .

EXPOSE 5001

ARG APP_MODULE=main:app
ARG PORT=5001
ARG HOST=0.0.0.0

ENV APP_MODULE=$APP_MODULE
ENV PORT=$PORT
ENV HOST=$HOST

ENTRYPOINT ["sh", "-c"]
CMD ["uvicorn $APP_MODULE --host $HOST --port $PORT"]