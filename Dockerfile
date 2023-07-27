FROM python:3.11.4

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /rollee

COPY . /rollee/

RUN pip install -r requirements.txt

