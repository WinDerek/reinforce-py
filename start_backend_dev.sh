#!/bin/bash

export FLASK_APP=app.py
export FLASK_DEBUG=1
python -u -m flask run --host 0.0.0.0 --port 41552
