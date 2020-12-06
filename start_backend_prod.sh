#!/bin/bash

export FLASK_APP=app.py
export FLASK_DEBUG=0

# Get the begin time
BEGIN=$(date +"%Y%m%d_%H%M%S")
echo Begin time: ${BEGIN}

mkdir -p log
nohup python -u -m flask run --host 0.0.0.0 --port 41552 > log/backend_${BEGIN}.log 2>&1 & disown
echo $! > log/backend_${BEGIN}_pid.txt
tail -f log/backend_${BEGIN}.log
