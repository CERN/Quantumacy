#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This code is part of QKDSimkit.
#
# SPDX-License-Identifier: MIT
#
# (C) Copyright 2021 CERN.

"""This module contains client's procedure to retrieve keys"""

import argparse
import http.client
import logging
import sys
import urllib.parse

import QKDSimkit.core as core
from QKDSimkit.core.qexceptions import boberror


def get_key(alice_address: str, channel_address: str, token: str, number: int, size: int):
    """Runs handshake and starts bob procedure

    Args:
        alice_address (str): address of server
        channel_address (str): address of channel
        token (str): pre shared token
        number (int): number of keys
        size (int): size of keys (bits)
    """
    try:
        hashed = core.utils.hash_token(token)
        params = urllib.parse.urlencode({'hashed': hashed})
        conn = http.client.HTTPConnection(f"{alice_address}")
        conn.request("GET", f"/hello?{params}")
        r = conn.getresponse()
        if r.status != 200:
            return r.status
        data = r.read().decode()
        proof = core.utils.decrypt(token, data)
        conn.close()
        hash_proof = core.utils.hash_token(proof)
        params = urllib.parse.urlencode({'number': number, 'size': size, 'hashed': hashed, 'hash_proof': hash_proof})
        conn.close()
        conn1 = http.client.HTTPConnection(f"{alice_address}")
        conn1.request("GET", f"/proof?{params}")
        r = conn1.getresponse()
    except Exception as e:
        logging.error("Error while connecting to server: " + str(e))
        sys.exit()
    if r.status == 200:
        try:
            key_list = []
            for n in range(number):
                res = core.bob.import_key(channel_address=channel_address, ID=hashed, size=size)
                if res == -1:
                    print("Can't exchange a safe key")
                if isinstance(res, bytes):
                    key_list.append(res.decode())
            return key_list
        except boberror as e:
            logging.error('Bob failed to exchange key: ' + str(e))
            sys.exit()
    else:
        return r.status


def manage_args():
    """Manages possible arguments and provides help messages"""

    parser = argparse.ArgumentParser(description='Client for Quantumacy')
    parser.add_argument('alice_address', type=str, help='Address of server/Alice [host:port]')
    parser.add_argument('channel_address', type=str, help='Address of channel [host:port]')
    parser.add_argument('-n', '--number', default=1, type=int, help="Number of keys (default: %(default)s)")
    parser.add_argument('-s', '--size', default=256, type=int, help="Size of keys (default: %(default)s)")
    return parser.parse_args()


def start_client(alice_address, channel_address, number, size):
    """Wrapper for get_key()
    Args:
        alice_address (str): address of server
        channel_address (str): address of channel
        number (int): number of keys
        size (int): size of keys (bits)
    """
    return get_key(alice_address, channel_address, '7KHuKtJ1ZsV21DknPbcsOZIXfmH1_MnKdOIGymsQ5aA=', number, size)


if __name__ == '__main__':
    args = manage_args()
    start_client(args.alice_address, args.channel_address, args.number, args.size)
