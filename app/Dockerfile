# nvidia cuda + ubuntu22.04
FROM nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04
ENV DEBIAN_FRONTEND=noninteractive

# Python
RUN apt-get update && \
    apt-get install -y python3 python3-pip

# ============================================================

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip3 install --upgrade pip setuptools

RUN pip3 install torch torchvision torchaudio

RUN apt-get update && apt-get install -y curl
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY ./requirements.txt /requirements.txt
RUN pip3 install --no-cache-dir -r /requirements.txt

ENV PYTHONPATH /project/source:/libs
WORKDIR /project/source

RUN mkdir -p /tmp/Ultralytics
COPY /source/utils/Arial.Unicode.ttf /tmp/Ultralytics
# RUN curl -o /tmp/Ultralytics/Arial.Unicode.ttf https://ultralytics.com/assets/Arial.Unicode.ttf
RUN fc-cache -f -v

# Разрешить докеру ловить видео
RUN adduser -u 5678 --disabled-password --gecos "" appuser && \
    adduser appuser video && \
    chown -R appuser /project
USER appuser
# RUN chmod -R 755 /tmp/Ultralytics



ENV YOLO_CONFIG_DIR=/tmp/Ultralytics


RUN mkdir -p /tmp/matplotlib
# RUN chmod -R 755 /tmp/matplotlib
ENV MPLCONFIGDIR=/tmp/matplotlib



# FROM python:3.12-slim

# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# RUN apt-get update && apt-get install -y curl
# RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# COPY ./requirements.txt /requirements.txt
# RUN pip3 install --no-cache-dir -r /requirements.txt

# ENV PYTHONPATH /project/source:/libs:/libs/vcelery

# WORKDIR /project/source
