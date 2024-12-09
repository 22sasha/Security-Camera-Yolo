FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN pip3 install --no-cache-dir -r /requirements.txt

ENV PYTHONPATH /project/source:/libs

WORKDIR /project/source
