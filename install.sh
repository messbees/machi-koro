#!/bin/bash
reset
echo "Begin Machi Koro installation..."

CLIENT="/client.py"
CLIENT_PATH="$PWD$CLIENT"
chmod a+x $CLIENT_PATH

SERVER_PATH="/server.py"
SERVER_PATH="$PWD$TP"
chmod a+x $SERVER_PATH

sudo ln -s $CLIENT_PATH /usr/bin/machi
sudo ln -s $SEVER_PATH /usr/bin/machi-server

echo "Links created."
