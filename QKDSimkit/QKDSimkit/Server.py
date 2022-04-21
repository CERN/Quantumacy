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

from aioredlock import Aioredlock


from QKDSimkit.Channel import start_channel
from QKDSimkit.core.qexceptions import cacheerror
from QKDSimkit.core.utils import generate_token

logger = logging.getLogger("QKDSimkit")

app = FastAPI()

cache = Cache(Cache.REDIS, endpoint="localhost", port=6379, namespace="QKDSimkit_server")

redis_lock = Aioredlock([('localhost', 6379)], retry_count=10, retry_delay_max=5, retry_delay_min=1)

origins = ["*"]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)


async def add_user(token: str):
    """Saves a token and its hash in memory

    Args:
        token (str): token representing a user
    """
    try:
        token = generate_token(token)
        lock = await redis_lock.lock('users')
        users = await cache.get('users')
        if not users:
            users = {}
        hashed = core.utils.hash_token(token)
        users[hashed] = token
        await cache.set('users', users)
        await redis_lock.unlock(lock)
    except Exception as e:
        raise cacheerror("Failed to add user in cache: " + str(e))


async def cache_set(key: str, value):
    '''Save a value in cahce

    Args:
         key (str): key
         value: value
    '''
    try:
        lock = await redis_lock.lock(key)
        await cache.set(key, value)
        await redis_lock.unlock(lock)
    except Exception as e:
        logger.error("Failed to set cache: " + str(e))


async def cache_get(key: str):
    '''Retrieve a value from cache

    Args:
        key (str): key
    '''
    try:
        lock = await redis_lock.lock(key)
        value = await cache.get(key)
        await redis_lock.unlock(lock)
        return value
    except ZeroDivisionError as e:
        logger.error("Failed to get cache: " + str(e))

async def start_alice(number: int, size: int, ID: str):
    """Imports keys from an alice node, saves keys in memory

    Args:
        number (int): number of keys
        size (int): size of keys (bits)
        ID (str): identifier (hash of token)
    """
    try:
        address = await cache_get('address')
        logger.error(address)
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
        try:
            lock_alice = await redis_lock.lock('alice')
            id_keys_map = await cache_get('id_keys')
            if not id_keys_map:
                id_keys_map = {}
            id_keys_map[ID] = key_list
            await cache_set('id_keys', id_keys_map)
            await redis_lock.lock(lock_alice)
        except Exception:
            logger.error("Failed to update key map in cache")
            sys.exit()
    except Exception as e:
        logger.error("Alice failed to exchange key " + str(e))
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
        # loop = asyncio.get_running_loop()
        # users = cache_get('users', loop)
        users = await cache_get('users')

        if hashed not in users.keys():
            return Response(status_code=404, content='Provided ID does not match any user')
        r = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(512))
        #lock_aut = loop.run_until_complete(redis_lock.lock("auth"))
        lock_aut = await redis_lock.lock("auth")
        map_hash_r = await cache_get('proof')
        if not map_hash_r:
            map_hash_r = {}
        map_hash_r[hashed] = core.utils.hash_token(r)
        await cache_set('proof', map_hash_r)
        #loop.run_until_complete(redis_lock.unlock(lock_aut))
        await redis_lock.unlock(lock_aut)
        response = core.utils.encrypt(users[hashed], r)
        return response
    except ZeroDivisionError as e:
        logger.error("Error while validating request " + str(e))


@app.get("/proof")
async def root(number: int, size: int, hashed: str, hash_proof: str, background_tasks: BackgroundTasks):
    """Checks handshake and starts alice

    Args:
        number (int): number of keys
        size (int): size of keys (bits)
        hashed (str): identifier (hash of token)
        hash_proof (str): hash of proof message
        background_tasks: background tasks
    """
    try:
        users = await cache_get('users')
        map_hash_r = await cache_get('proof')
    except Exception as e:
        logger.error("Failed to retrieve data from cache: " + str(e))
        return Response(status_code=500, content='Internal server error')
    if hashed in users.keys() and hash_proof == map_hash_r[hashed]:
        background_tasks.add_task(start_alice, number, size, hashed)
        return "Verified!"
    return Response(status_code=404, content='Provided ID does not match any user')


@app.get("/get_key")
async def getkey(password: Optional[str] = None):
    """Retrieves keys from server

    Args:
        password (str): hashed token
    """
    try:
        id_keys_map = await cache_get('id_keys')
    except Exception as e:
        logger.error("Failed to retrieve key map from cache: " + str(e))
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
    """ Synchronous wrapper for get_key

    Returns:
          keys: list of keys for the given ID
    """
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
        # loop = asyncio.new_event_loop()
        # add_user('token', loop)
        # cache_set('address', channel_address, loop)
        asyncio.run(add_user('token'))
        asyncio.run(cache_set('address', channel_address))
    except cacheerror as ce:
        logger.error(str(ce))
        sys.exit()
    _thread = Thread(target=start_channel, args=(channel_address, noise, eve))
    _thread.daemon = True
    _thread.start()
    time.sleep(0.5)
    if _thread.is_alive():
        try:
            uvicorn.run('QKDSimkit.Server:app', host=address.split(':')[0], port=int(address.split(':')[1]), workers=1)
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
        asyncio.run(cache_set('address', channel_address))
    except cacheerror as ce:
        logger.error(str(ce))
        sys.exit()
    try:
        uvicorn.run('QKDSimkit.Server:app', host=address.split(':')[0], port=int(address.split(':')[1]))
    except Exception as e:
        logger.error("Error on while running server: " + str(e))
        sys.exit()
