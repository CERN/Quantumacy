#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
# ----------------------------------------------------------------------------
# Created By  : José Cabrero-Holgueras
# Created Date: 01/2022
# Copyright: CERN
# License: MIT
# version ='1.0'
# ---------------------------------------------------------------------------

import socket
def resolve(domain):
    ip = socket.getaddrinfo(domain, 0, socket.AddressFamily.AF_INET, socket.SocketKind.SOCK_STREAM)[0][4][0]
    return ip

ALICE_IP = resolve('olvm-livinglab-03')
ALICE_PORT = 5002
ALICE_ADDRESS = "{}:{}".format(ALICE_IP, ALICE_PORT)

CHANNEL_IP = resolve('olvm-livinglab-03')
CHANNEL_PORT = 5000
CHANNEL_ADDRESS = "{}:{}".format(CHANNEL_IP, CHANNEL_PORT)

LINK_1_TOKEN = 'pre-sto-token'
LINK_2_TOKEN = 'pro-sto-token'
CLIENT_ROLE = 'CLIENT'
SERVER_ROLE = 'SERVER'
ROLE = None

# ROLE = SERVER_ROLE # COMMENT THIS LINE IF IT IS THE CLIENT
# ROLE = CLIENT_ROLE # COMMENT THIS LINE IF IT IS THE SERVER
QKD_ENABLE = False