#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
# ----------------------------------------------------------------------------
# Created By  : José Cabrero-Holgueras
# Created Date: 01/2022
# Copyright: CERN
# License: MIT
# version ='1.0'
# ---------------------------------------------------------------------------

import secrets
from flask import Flask, redirect, request, jsonify, session, Response
from flask import url_for, render_template, send_from_directory
import os, json


from python.go import *
from python.qkd import qkd_encrypt, qkd_decrypt, random_string, http_send, http_file_request, register_user
from python.config import * 

#setting the flask instance
app = Flask(__name__)

ImageList = os.listdir(DOCKER_DIR + "data/dataset")

@app.route("/register", methods=["GET"])
def register():
    token = request.args.get('token')
    register_user(token)
    return Response("OK", status=200)

@app.route("/request", methods=["GET"])
def http_request():
    path = request.args.get('src').replace("./", " ") # forces an error if malicious
    token = request.args.get('token')
    with open(path, 'rb') as file:
        data = file.read()
    enc_data = qkd_encrypt(data, token)
    dic = {
        'data': enc_data.decode('utf-8')
    }
    return Response(json.dumps(dic), status=200)

@app.route("/store", methods=["POST"])
def http_recv():
    dic = json.loads(request.get_json())
    token = dic['token']
    dst = dic['dst'].replace("./"," ") # forces an error if malicious
    enc_data = dic['data'].encode('utf-8')
    data = qkd_decrypt(enc_data, token)
    with open(dst, 'wb+') as file:
        file.write(data)
    return Response("OK", status=200)


#By default the server is running at port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=STORAGE_PORT)
