#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This code is part of QKDSimkit.
#
# SPDX-License-Identifier: MIT
#
# (C) Copyright 2021 CERN.

import argparse
import asyncio
import os
import random
import string

import uvicorn

import QKDSimkit.core as core

from aiocache import Cache
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from threading import Thread

from QKDSimkit.Channel import start_channel

data_directory = os.path.dirname(os.path.realpath(__file__)) + '/../data/'

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


async def add_user(token):
    users = {}
    hashed = core.utils.hash_token(token)
    users[hashed] = token
    await cache.set('users', users)


async def add_channel(address):
    await cache.set('address', address)


async def start_alice(number: int, size: int, ID: str):
    id_keys_map = await cache.get('id_keys')
    if not id_keys_map:
        id_keys_map = {}
    address = await cache.get('address')
    if not address:
        raise Exception
    key_list = []
    for i in range(number):
        res = core.alice.import_key(channel_address=address, ID=ID, size=size)
        if res == -1:
            print("Can't exchange a safe key")
        if isinstance(res, bytearray):
            key_list.append(res.decode())
    id_keys_map[ID] = key_list
    await cache.set('id_keys', id_keys_map)


@app.get("/hello")
async def root(hashed: str):
    users = await cache.get('users')
    if hashed not in users.keys():
        return Response(status_code=404, content='Provided ID does not match any user')
    r = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(512))
    map_hash_r = await cache.get('proof')
    if not map_hash_r:
        map_hash_r = {}
    map_hash_r[hashed] = core.utils.hash_token(r)
    await cache.set('proof', map_hash_r)
    return core.utils.encrypt(users[hashed], r)


@app.get("/proof")
async def root(number: int, size: int, hashed: str, hash_proof: str, background_tasks: BackgroundTasks):
    users = await cache.get('users')
    map_hash_r = await cache.get('proof')
    if hashed in users.keys() and hash_proof == map_hash_r[hashed]:
        background_tasks.add_task(start_alice, number, size, hashed)
        return "Verified!"
    return Response(status_code=404, content='Provided ID does not match any user')


@app.get("/get_key")
async def root(ID: str = 'id'):
    id_keys_map = await cache.get('id_keys')
    if ID not in id_keys_map.keys():
        raise HTTPException(status_code=404, detail="No keys for the given ID")
    return id_keys_map[ID]


@app.middleware("http")
async def filter_get_key(request: Request, call_next):
    if request.client.host != '127.0.0.1' and request.url.path == '/get_key':
        response = Response(status_code=403, content='Forbidden')
    else:
        response = await call_next(request)
    return response


def manage_args():
    parser = argparse.ArgumentParser(description='Server for Quantumacy')
    parser.add_argument('-a', '--address', default='127.0.0.1:5002', type=str,
                        help='Bind socket to this address (default: %(default)s)')
    channels = parser.add_subparsers(title='Channel type', dest='channel_type', required=True,
                                     help='Specify where the channel is (required)')
    parser_l = channels.add_parser('local', help='Run the channel on this machine')
    parser_l.add_argument('-ca', '--channel_address', default=':5000', type=str,
                          help='Bind socket to this address (default: %(default)s)')
    parser_l.add_argument('-n', '--noise', default=0.0, type=float,
                          help='Set a noise value for channel, type a float number in [0,1] (default: %(default)s)')
    parser_l.add_argument('-e', '--eve', action='store_true',
                          help='Add an eavesdropper to the channel')
    parser_e = channels.add_parser('external', help='Connect to an external channel')
    parser_e.add_argument('-ca', '--channel_address', type=str, required=True, help='Address of channel [host:port]')
    return parser.parse_args()


def start_server_and_channel(channel_address, noise, eve, address):
    asyncio.run(add_user('7KHuKtJ1ZsV21DknPbcsOZIXfmH1_MnKdOIGymsQ5aA='))
    asyncio.run(add_channel(channel_address))
    _thread = Thread(target=start_channel, args=(channel_address, noise, eve))
    _thread.daemon = True
    _thread.start()
    uvicorn.run('QKDSimkit.Server:app', host=address.split(':')[0], port=int(address.split(':')[1]))


def start_server(channel_address, address):
    asyncio.run(add_channel(channel_address))
    uvicorn.run('QKDSimkit.Server:app', host=address.split(':')[0], port=int(address.split(':')[1]))


if __name__ == "__main__":
    args = manage_args()
    if args.channel_type == 'local':
        start_server_and_channel(args.channel_address, args.noise, args.eve, args.address)
    if args.channel_type == 'external':
        start_server(args.channel_address, args.address)