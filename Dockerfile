FROM python:3.12.3

ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

WORKDIR /app

COPY config config/
COPY src src/
COPY .env .


