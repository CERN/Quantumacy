#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
# ----------------------------------------------------------------------------
# Created By  : José Cabrero-Holgueras
# Created Date: 01/2022
# Copyright: CERN
# License: MIT
# version ='1.0'
# ---------------------------------------------------------------------------

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import os, random, string, base64, requests, json
from python.qkd_config import ALICE_ADDRESS, CHANNEL_ADDRESS, QKD_ENABLE, ROLE, CLIENT_ROLE, SERVER_ROLE, LINK_1_TOKEN, LINK_2_TOKEN

import asyncio
from QKDSimkit.Server import add_user, get_key_cli, start_server_and_channel
from QKDSimkit.Client import start_client

# if ROLE is SERVER_ROLE:
#     #this part only once to add user in the dict in memory
#     asyncio.run(add_user(LINK_1_TOKEN))
#     asyncio.run(add_user(LINK_2_TOKEN)) 

def register_user(user_id):
    asyncio.wait(asyncio.run(add_user(LINK_1_TOKEN + user_id))) # Register a client-storage with id 
    asyncio.wait(asyncio.run(add_user(LINK_2_TOKEN + user_id))) # Register a storage-server link with id

def register_user_client(machine, port, user_id):
    if not QKD_ENABLE:
        return
    url = "http://{}:{}/register?token={}".format(machine, port, user_id)
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception
    

def get_key_as_server(token):

    #if you run in olvm machines you don't need this
    #start_server_and_channel(CHANNEL_ADDRESS, False, False, address) #put False in noise and eve

    #retrieve key
    key = get_key_cli(token)
    print(key)
    return key[0]


def get_key_as_client(token): 
    
    key = start_client(ALICE_ADDRESS, CHANNEL_ADDRESS, 1, 1 << 8, token, False)
    return key[0]

def qkd_encrypt(data, token):
    print("ENCRYPT USING TOKEN:", token)

    key = None
    if not QKD_ENABLE or token is None:
        password = b"password"
        salt = b'1234567890123456'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=390000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
    elif ROLE is SERVER_ROLE:
        key = get_key_as_server(token)
    
    else:
        key = get_key_as_client(token)
    
    print("ENCRYPT USING KEY: ", key)
    # using the generated key
    fernet = Fernet(key)
    
    # encrypting the file
    encrypted = fernet.encrypt(data)
    return encrypted

def qkd_decrypt(data, token, key=None):

    print("DECRYPT USING TOKEN:", token)

    if not key is None:
        # If key is given by user, we do nothing
        pass
    elif not QKD_ENABLE or token is None:
        password = b"password"
        salt = b'1234567890123456'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=390000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
    elif ROLE is SERVER_ROLE:
        key = get_key_as_server(token)
    
    else: 
        key = get_key_as_client(token)
    print("DECRYPT USING KEY: ", key)
    # using the generated key
    fernet = Fernet(key)

    # decrypting the file
    decrypted = fernet.decrypt(data)
    return decrypted

def random_string(l=10):
    return ''.join((random.choice(string.ascii_lowercase) for x in range(l)))
    
def scp_move(src, dest):
    os.system("scp {} {}".format(src, dest))


def http_send(machine, port, src, dest, token=None):
    with open(src, 'rb') as file:
        data = file.read()
    
    enc_data = qkd_encrypt(data, token)
    dic = {
        'dst': dest,
        'data': enc_data.decode('utf-8'),
        'token': token
    }
    url = "http://{}:{}/store".format(machine, port)
    
    response = requests.post(url, json=json.dumps(dic))
    return response

def http_file_request(machine, port, src, dest, token=None):
    key = None
    if  QKD_ENABLE and ROLE is CLIENT_ROLE:
        # In requests to server, it is needed to be done first by the client
        key = get_key_as_client(token) 
    url = "http://{}:{}/request?src={}&token={}".format(machine, port, src, token)
    response = requests.get(url)
    dic = json.loads(response.content)
    enc_data = dic['data'].encode('utf-8')
    data = qkd_decrypt(enc_data, token, key=key)
    with open(dest, 'wb+') as file:
        file.write(data)
