#!/bin/bash

sudo apt update
sudo apt-get install -y python3 python3-virtualenv python3-pip git
sudo apt-get install -y ca-certificates curl gnupg screen
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /usr/share/keyrings/nodesource.gpg
NODE_MAJOR=18
echo "deb [signed-by=/usr/share/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list
sudo apt update
sudo apt install -y nodejs
npm install yarn -g --force
git clone https://github.com/henrytriplette/solar-meter-server
cd solar-meter-server
virtualenv -p python3 venv
source venv/bin/activate
pip3 install -r requirements.txt
cd client
yarn
yarn build
cd ..
