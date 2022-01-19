#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This code is part of QKDSimkit.
#
# SPDX-License-Identifier: MIT
#
# (C) Copyright 2021 CERN.

"""This module contains methods to operate a p2p node"""

import argparse
import asyncio
import logging
import json
import sys

import uvicorn

from aiocache import Cache
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

import QKDSimkit.core as core
from QKDSimkit.core.qexceptions import aliceerror, cacheerror

logger = logging.getLogger("QKDSimkit")


cache = Cache(Cache.REDIS, endpoint="localhost", port=6379, namespace="p2p_server")


alice_app = FastAPI()
bob_app = FastAPI()


async def answer_get(number: int, size: int, ID: str, type: str):
    """Starts a node

    Args:
        number (int): number of keys
        size (int): size of keys (bits)
        ID (str): identifier of a pair of nodes
        type (str): alice or bob (sender or receiver)
    Returns:
        keys
    """
    answer = {}
    keys = []
    try:
        address = await cache.get("channel_address")
    except Exception:
        logger.error("Failed to retrieve address from cache")
        sys.exit()
    try:
        for i in range(number):
            if type == 'Alice':
                key = core.alice.import_key(channel_address=address, ID=ID, size=size)
            if type == 'Bob':
                key = core.bob.import_key(channel_address=address, ID=ID, size=size)
            if key != -1:
                keys.append({"key_ID": i, "key": key})
        answer["keys"] = keys
        return answer
    except aliceerror as e:
        logger.error(type + " failed to exchange key: " + e)
        sys.exit()


@alice_app.get("/test")
async def root(number: int = 1, size: int = 256, ID: str = 'id'):
    """http request handler for alice

        Args:
            number (int): number of keys
            size (int): size of keys (bits)
            ID (str): identifier of a pair of nodes
        Returns:
            keys
    """
    try:
        return await answer_get(number, size, ID, 'Alice')
    except Exception:
        return Response(status_code=500, content='Internal server error')


@bob_app.get("/test")
async def root(number: int = 1, size: int = 256, ID: str = 'id'):
    """http request handler for bob

        Args:
            number (int): number of keys
            size (int): size of keys (bits)
            ID (str): identifier of a pair of nodes
        Returns:
            keys
    """
    try:
        return await answer_get(number, size, ID, 'Bob')
    except Exception:
        return Response(status_code=500, content='Internal server error')

origins = [
    "*"
]

alice_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bob_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def manage_args():
    """Manages possible arguments and provides help messages"""

    parser = argparse.ArgumentParser(description='Server for Quantumacy')
    parser.add_argument('node', choices=['alice', 'bob'],
                       help='Choose how to run this node')
    parser.add_argument('-c', '--channel_address', default=':5000', type=str,
                        help='Specify the address of the channel [host:port]')
    parser.add_argument('-a', '--address', default='127.0.0.1:5003', type=str,
                        help='Bind socket to this address (default: %(default)s)')
    return parser.parse_args()


def start_p2p(node: str, address: str, channel_address: str):
    """Starts server

    Args:
        node (str): type of node [alice, bob]
        address (str): where to bind socket
    """
    asyncio.run(cache.set('channel_address', channel_address))
    uvicorn.run('QKDSimkit.p2p_servers:{}_app'.format(node), host=address.split(':')[0], port=int(address.split(':')[1]))


if __name__ == '__main__':
    args = manage_args()
    start_p2p(args.node, args.address)
