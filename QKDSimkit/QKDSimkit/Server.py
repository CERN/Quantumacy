#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This code is part of QKDSimkit.
#
# SPDX-License-Identifier: MIT
#
# (C) Copyright 2021 CERN.

"""This module contains server's APIs and method to run it"""

import argparse
import asyncio
import logging
import sys
import time
import random
import string
import uvicorn

import QKDSimkit.core as core

from aiocache import Cache
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from threading import Thread
from typing import Optional

from QKDSimkit.Channel import start_channel
from QKDSimkit.core.qexceptions import cacheerror
from QKDSimkit.core.utils import generate_token

logger = logging.getLogger("QKDSimkit")


app = FastAPI()

cache = Cache(Cache.REDIS, endpoint="localhost", port=6379, namespace="main")

origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def add_user(password: str):
    """Saves a token and its hash in memory"""
    try:
        token = generate_token(password)
        users = await cache.get('users')
        if not users:
            users = {}
        hashed = core.utils.hash_token(token)
        users[hashed] = token
        await cache.set('users', users)
    except Exception as e:
        raise cacheerror("Failed to add user in cache: " + str(e))


async def add_channel(address: str):
    """Saves an address in memory"""
    try:
        await cache.set('address', address)
    except Exception:
        raise cacheerror("Failed to add channel in cache")



async def start_alice(number: int, size: int, ID: str):
    """Imports keys from an alice node, saves keys in memory

    Args:
        number (int): number of keys
        size (int): size of keys (bits)
        ID (str): identifier (hash of token)
    """
    try:
        id_keys_map = await cache.get('id_keys')
        if not id_keys_map:
            id_keys_map = {}
    except Exception:
        logger.error("Failed to retrieve key map from cache")
        sys.exit()
    try:
        address = await cache.get('address')
        if not address:
            raise Exception
    except Exception:
        logger.error("Failed to retrieve address from cache")
        sys.exit()
    key_list = []
    try:
        for i in range(number):
            res = core.alice.import_key(channel_address=address, ID=ID, size=size)
            if res == -1:
                print("Can't exchange a safe key")
            if isinstance(res, bytes):
                key_list.append(res.decode())
        id_keys_map[ID] = key_list
    except Exception as e:
        logger.error("Alice failed to exchange key " + str(e))
        return
    try:
        await cache.set('id_keys', id_keys_map)
    except Exception:
        logger.error("Failed to set key map in cache")
        sys.exit()


@app.get("/hello")
async def root(hashed: str):
    """Handshake request

    Args:
        hashed (str): hash of a pre-shared token

    Returns:
        message (str): test message for handshake
    """
    try:
        users = await cache.get('users')
        if hashed not in users.keys():
            return Response(status_code=404, content='Provided ID does not match any user')
        r = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(512))
        map_hash_r = await cache.get('proof')
        if not map_hash_r:
            map_hash_r = {}
        map_hash_r[hashed] = core.utils.hash_token(r)
        await cache.set('proof', map_hash_r)
        response = core.utils.encrypt(users[hashed], r)
        return response
    except Exception:
        logger.error("Error while validating request")


@app.get("/proof")
async def root(number: int, size: int, hashed: str, hash_proof: str, background_tasks: BackgroundTasks):
    """Chacek handshake and starts alice

    Args:
        number (int): number of keys
        size (int): size of keys (bits)
        hashed (str): identifier (hash of token)
        hash_proof (str): hash of proof message
        background_tasks: background tasks
    """
    try:
        users = await cache.get('users')
        map_hash_r = await cache.get('proof')
    except Exception:
        logger.error("Failed to retrieve data from cache")
        return Response(status_code=500, content='Internal server error')
    if hashed in users.keys() and hash_proof == map_hash_r[hashed]:
        background_tasks.add_task(start_alice, number, size, hashed)
        return "Verified!"
    return Response(status_code=404, content='Provided ID does not match any user')


@app.get("/get_key")
async def getkey(password: Optional[str] = None):
    """Retrieves key from server

    Args:
        ID (str): hashed token
    """
    try:
        id_keys_map = await cache.get('id_keys')
    except Exception:
        logger.error("Failed to retrieve key map from cache")
        return Response(status_code=404, content="No keys available")
    if password is None:
        return id_keys_map
    else:
        ID = core.utils.hash_token(generate_token(password))

        if ID not in id_keys_map.keys():
            return Response(status_code=404, content="No keys for the given ID")
        else:
            return id_keys_map[ID]


@app.middleware("http")
async def filter_get_key(request: Request, call_next):
    if request.client.host != '127.0.0.1' and (request.url.path == '/get_key'):
        response = Response(status_code=403, content='Forbidden')
    else:
        response = await call_next(request)
    return response


def get_key_cli(id):
    keys = asyncio.run(getkey(id))
    logger.info(keys)
    return keys


def start_server_and_channel(channel_address: str, noise: float, eve: bool, address: str):
    """Starts both server and channel

    Returns:
        channel_address (str): address of channel
        noise (float): ratio of noise in channel
        eve (bool): simulate an eavesdropper in channel
        address (str): where to bind this server
    """
    try:
        asyncio.run(add_user('token'))
        asyncio.run(add_channel(channel_address))
    except cacheerror as ce:
        logger.error(str(ce))
        sys.exit()
    _thread = Thread(target=start_channel, args=(channel_address, noise, eve))
    _thread.daemon = True
    _thread.start()
    time.sleep(0.5)
    if _thread.is_alive():
        try:
            uvicorn.run('QKDSimkit.Server:app', host=address.split(':')[0], port=int(address.split(':')[1]))
        except Exception as e:
            logger.error("Error on while running server: " + str(e))
            sys.exit()


def start_server(channel_address, address):
    """Starts server and connect to an external channel

    Args:
        channel_address (str): address of channel
        address (str): where to bind this server
    """
    try:
        asyncio.run(add_user('token'))
        asyncio.run(add_channel(channel_address))
    except cacheerror as ce:
        logger.error(str(ce))
        sys.exit()
    try:
        uvicorn.run('QKDSimkit.Server:app', host=address.split(':')[0], port=int(address.split(':')[1]))
    except Exception:
        logger.error("Error on while running server")
        sys.exit()
