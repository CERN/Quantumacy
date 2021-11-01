#!/bin/bash

cd QKDSimChannels
python QKD-Channel.py &

cd ../QKDSimClients
uvicorn QKD_Alice:app --host 127.0.0.1 --port 8000 --reload &
uvicorn QKD_Bob:app --host 127.0.0.1 --port 8001 --reload &