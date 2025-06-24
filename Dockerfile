FROM python:3.12.3

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
RUN apt-get update && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY src/ src/
COPY config/ config/
COPY .env .

