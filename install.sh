#!/bin/bash

python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
chmod +x gopherus3.py
# sudo ln -sf $(pwd)/gopherus3.py /usr/local/bin/gopherus3
echo "Gopherus3 installed"
