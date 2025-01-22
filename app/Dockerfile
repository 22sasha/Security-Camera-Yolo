# nvidia cuda + ubuntu22.04
FROM nvidia/cuda:12.6.3-cudnn-devel-ubuntu24.04
ENV DEBIAN_FRONTEND=noninteractive

RUN rm /etc/apt/sources.list.d/cuda.list

# Python
RUN apt-get update && \
    apt-get install -y \
    python3.12 \
    python3.12-venv \
    python3-pip \
    curl \
    ffmpeg \
    libsm6 \
    libxext6


# ============================================================

RUN python3 -m venv /venv
RUN /venv/bin/python -m pip install --upgrade pip
RUN /venv/bin/pip install torch torchvision torchaudio

COPY ./requirements.txt /requirements.txt
RUN /venv/bin/pip install --no-cache-dir -r /requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

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
