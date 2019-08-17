#!/bin/bash


cd ..
mv src Mira
mkdir -p src
cd Mira

export FLASK_APP=app.py
export FLASK_DEBUG=1
python -m flask run --host=0.0.0.0 --port=5000