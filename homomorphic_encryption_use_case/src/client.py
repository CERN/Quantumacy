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
#flask module for the http requests
from flask import Flask, redirect, request, jsonify, session, Response
from flask import url_for, render_template, send_from_directory
import os, json

from python.go import *
from python.qkd import qkd_encrypt, qkd_decrypt, random_string, http_send, http_file_request, register_user_client
from python.config import * 
from python.qkd_config import LINK_1_TOKEN

#setting the flask instance
app = Flask(__name__)

ImageList = os.listdir(DOCKER_DIR + "data/dataset")

@app.route("/keygen", methods=["GET"])
def http_keygen():
    print("Executing Keygen")
    keygen(params = "/tmp/p", sk = "/tmp/p", pk = "/tmp/p", rlk = "/tmp/p", gks = "/tmp/p")
    return Response("OK", status=200)

@app.route("/images", methods=["GET"])
def http_list_imgs():
    print("Executing List Images")
    print(ImageList)
    return jsonify(ImageList)

@app.route("/get-image/<image_name>", methods=["GET"])
def get_image(image_name):

    if not image_name in ImageList:
        return Response("Image Not Found", status=404)
        
    return send_from_directory(DOCKER_DIR + "/data/dataset/", image_name, mimetype='image/png')

@app.route("/encrypt/<image_name>", methods=["GET"])
def http_encrypt(image_name):
    img = image_name.replace("./"," ") # forces an error if malicious
    if not img in ImageList:
        return Response("Invalid Image", status=403)

    file_id = random_string()
    img_src = DOCKER_DIR + 'data/dataset/%s' %(img)
    enc_dest = DOCKER_DIR + 'data/preprocessing/img_%s.enc' %(file_id)
    sto_dest = DOCKER_DIR + 'data/storage/img_%s.enc' %(file_id)

    register_user_client(STORAGE_MACHINE, STORAGE_PORT, file_id)

    encrypt(plaintext=img_src, ciphertext=enc_dest)
    


    http_send(STORAGE_MACHINE, STORAGE_PORT, enc_dest, sto_dest, LINK_1_TOKEN + file_id)

    dic = {
        'file_id': file_id
    }

    return Response(json.dumps(dic), status=200)


@app.route("/decrypt/<id>", methods=["GET"])
def http_decrypt(id):
    file_id = id.replace("./"," ")
    result_src = DOCKER_DIR + 'data/storage/result_%s.enc' %(file_id)
    result_dest = DOCKER_DIR + 'data/storage/result_%s.enc' %(file_id)
    http_file_request(STORAGE_MACHINE, STORAGE_PORT, result_src, result_dest, LINK_1_TOKEN + file_id)

    ret = decrypt(ciphertext=result_dest)

    return Response("The private algorithm predicted: {}".format(ret), status=200)


#By default the server is running at port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PREPROCESSING_PORT)
