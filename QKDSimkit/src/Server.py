import uvicorn
import os
import asyncio
import random
import string
import json
import argparse
import core
import Channel
from threading import Thread
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from aiocache import Cache

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
    parser.add_argument('--host', default='127.0.0.1', type=str,
                        help='Bind socket to this host (default: %(default)s)')
    parser.add_argument('--port', default='5002', type=str,
                        help='Bind socket to this port (default: %(default)s)')
    parser.add_argument('-t', '--token', default='7KHuKtJ1ZsV21DknPbcsOZIXfmH1_MnKdOIGymsQ5aA=', type=str,
                        help='Auth token, for development purposes a default token is provided')
    channels = parser.add_subparsers(title='Channel type', dest='channel_type', required=True,
                                     help='Specify where the channel is (required)')
    parser_l = channels.add_parser('l', help='Run the channel on this machine')
    parser_l.add_argument('-ch', '--channel_host', default='', type=str,
                          help='Bind socket to this host (default: %(default)s)')
    parser_l.add_argument('-cp', '--channel_port', default='5000', type=str,
                        help='Bind socket to this port (default: %(default)s)')
    parser_l.add_argument('-n', '--noise', default=0.0, type=float,
                          help='Set a noise value for channel, type a float number in [0,1] (default: %(default)s)')
    parser_l.add_argument('-e', '--eve', action='store_true',
                          help='Add an eavesdropper to the channel')
    parser_e = channels.add_parser('e', help='Connect to an external channel')
    parser_e.add_argument('-ca', '--channel_address', type=str, required=True, help='Address of channel [host:port]')
    return parser.parse_args()


if __name__ == "__main__":
    args = manage_args()
    asyncio.run(add_user(args.token))
    if args.channel_type == 'l':
        address = '{h}:{p}'.format(h=args.channel_host, p=args.channel_port)
        asyncio.run(add_channel(address))
        _thread = Thread(target=Channel.run_channel, args=(args.channel_host, args.channel_port, args.noise,
                                                            args.eve))
        _thread.daemon = True
        _thread.start()
    else:
        asyncio.run(add_channel(args.channel_address))
    uvicorn.run('Server:app', host=args.host, port=int(args.port))
