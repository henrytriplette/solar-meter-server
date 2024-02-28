#!/bin/bash

sudo apt update
sudo apt-get install -y python3 python3-virtualenv python3-pip
git clone https://github.com/henrytriplette/solar-meter-server
cd solar-meter-server
virtualenv -p python3 venv
source venv/bin/activate
pip3 install -r requirements.txt
