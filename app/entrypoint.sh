#!/bin/bash

sleep 3


alembic upgrade head

# python3 utils/check.py
python3 main.py

while true; do sleep 1000; done