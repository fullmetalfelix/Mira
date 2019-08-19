#!/bin/bash


cd ..
mv src Mira
mkdir -p src
cd Mira

mv config-rahti.py config.py
mkdir models
curl 'https://lilablobssc.blob.core.windows.net/models/camera_traps/megadetector/megadetector_v3.pb' > models/megadetector_v3.pb


export FLASK_APP=app.py
export FLASK_DEBUG=1
python -m flask run --host=0.0.0.0 --port=5000
