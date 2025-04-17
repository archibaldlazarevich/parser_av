FROM python:3.12.3

ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app/
RUN apt-get update && \
    pip install --upgrade pip && \
    pip install -r /app/requirements.txt && \
    apt-get install -y locales && \
    sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen && \
    dpkg-reconfigure --frontend=noninteractive locales


WORKDIR /app

COPY config config/
COPY src src/
COPY .env .


