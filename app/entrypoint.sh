#!/bin/bash

sleep 3


/venv/bin/alembic upgrade head

# sleep infinity
# python3 utils/check.py
/venv/bin/python3 main.py

while true; do sleep 1000; done