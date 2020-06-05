#!/bin/bash

export FLASK_APP=app.py
export FLASK_DEBUG=0

# Get the begin time
BEGIN=$(date +"%Y%m%d_%H%M%S")
echo Begin time: ${BEGIN}

mkdir -p log
stdbuf -i0 -o0 -e0 nohup python -m flask run --host 0.0.0.0 --port 45679 > log/flask_server_${BEGIN}.log 2>&1 & disown
echo $! > log/flask_server_${BEGIN}_pid.txt
tail -f log/flask_server_${BEGIN}.log
