#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
# ----------------------------------------------------------------------------
# Created By  : José Cabrero-Holgueras
# Created Date: 01/2022
# Copyright: CERN
# License: MIT
# version ='1.0'
# ---------------------------------------------------------------------------

import os

def keygen(params = None, sk = None, pk = None, rlk = None, gks = None):
    command = "./bin/keygen"
    if not params is None:
        command += " --p={}".format(params)
    if not sk is None:
        command += " --sk={}".format(sk)  
    if not pk is None:
        command += " --pk={}".format(pk)  
    if not rlk is None:
        command += " --rlk={}".format(rlk)  
    if not gks is None:
        command += " --gks={}".format(gks)  
    print("[COMMAND]: " + command)
    try:
        os.system(command)
    except os.error as E:
        print(E)
    print("[DONE][COMMAND]: " + command)
    

def encrypt(plaintext=None, ciphertext=None, pk=None, params=None):

    command = "./bin/encryptor"
    if not params is None:
        command += " --p={}".format(params)
    if not pk is None:
        command += " --pk={}".format(pk)  
    if not plaintext is None:
        command += " --i={}".format(plaintext)  
    if not ciphertext is None:
        command += " --c={}".format(ciphertext)
    print("[COMMAND]: " + command)
    try:
        os.system(command)
    except os.error as E:
        print(E)
    print("[DONE][COMMAND]: " + command)

def decrypt(ciphertext=None, sk=None, params=None):

    command = "./bin/decryptor"
    if not params is None:
        command += " --p={}".format(params)
    if not sk is None:
        command += " --sk={}".format(sk)  
    if not ciphertext is None:
        command += " --oc={}".format(ciphertext)  
    print("[COMMAND]: " + command)
    status = os.system(command)
    print("[DONE][COMMAND]: " + command)
    return os.WEXITSTATUS(status)


def runtime(input_ciphertext=None, output_ciphertext=None, rlk=None, gks=None, params=None):

    command = "./bin/runtime"
    if not params is None:
        command += " --p={}".format(params)
    if not rlk is None:
        command += " --rlk={}".format(rlk)  
    if not gks is None:
        command += " --gks={}".format(gks)
    if not input_ciphertext is None:
        command += " --ic={}".format(input_ciphertext)  
    if not output_ciphertext is None:
        command += " --oc={}".format(output_ciphertext)  
    print("[COMMAND]: " + command)
    os.system(command)
    print("[DONE][COMMAND]: " + command)