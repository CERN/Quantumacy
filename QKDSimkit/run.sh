#!/bin/bash

cd QKDSimChannels
python3 QKD-Channel.py &

cd ../Server_Client_wrapper
python3 Server.py &
python3 Client.py &