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
from python.qkd import qkd_encrypt, qkd_decrypt, random_string, http_send, http_file_request
from python.config import * 
from python.qkd_config import LINK_2_TOKEN

#setting the flask instance
app = Flask(__name__)

@app.route("/runtime/<id>", methods=["GET"])
def http_runtime(id):
    file_id = id.replace("./"," ")
    ct_src = DOCKER_DIR + 'data/storage/img_%s.enc' %(file_id)
    ct_dest = DOCKER_DIR + 'data/processing/img_%s.enc' %(file_id)
    result_src = DOCKER_DIR + 'data/processing/result_%s.enc' %(file_id)
    result_dest = DOCKER_DIR + 'data/storage/result_%s.enc' %(file_id)
    http_file_request(STORAGE_MACHINE, STORAGE_PORT, ct_src, ct_dest, LINK_2_TOKEN + file_id)

    runtime(input_ciphertext=ct_dest, output_ciphertext=result_src)

    http_send(STORAGE_MACHINE, STORAGE_PORT, result_src, result_dest, LINK_2_TOKEN + file_id)

    dic = {
        'file_id': file_id
    }

    return Response(json.dumps(dic), status=200)



#By default the server is running at port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PROCESSING_PORT)
