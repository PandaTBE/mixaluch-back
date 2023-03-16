# Dockerfile
FROM python:3.10

WORKDIR /app

RUN apt-get update -y
RUN apt-get upgrade -y

COPY ./requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .