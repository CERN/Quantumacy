import uvicorn
import os
import asyncio
import random
import string

from QKDSimkit.QKDSimClients.utils import hash_token, encrypt
from QKDSimkit.QKDSimClients.QKD_Alice import import_key
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
from aiocache import Cache

directory = os.path.dirname(os.path.realpath(__file__)) + '/server_data/'


def add_user(token):
    hashed = hash_token(token)
    users[hashed] = token


async def start_alice(number: int, size: int, ID: str):
    id_keys_map = await cache.get('id_keys')
    if not id_keys_map:
        id_keys_map = {}
    key_list = []
    for n in range(number):
        key_list.append(import_key(ID=ID, size=size).decode())
    id_keys_map[ID] = key_list
    await cache.set('id_keys', id_keys_map)


class qkdParams(BaseModel):
    number: int = 1
    size: int = 256
    ID: str = 'id'


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


@app.get("/hello")
async def root(hashed: str):
    users = await cache.get('users')
    if hashed not in users.keys():
        return Response(status_code=404, content='Provided ID does not match any user')
    r = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(512))
    map_hash_r = await cache.get('proof')
    if not map_hash_r:
        map_hash_r = {}
    map_hash_r[hashed] = hash_token(r)
    await cache.set('proof', map_hash_r)
    return encrypt(users[hashed], r)


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


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    users = {}
    add_user('7KHuKtJ1ZsV21DknPbcsOZIXfmH1_MnKdOIGymsQ5aA=')
    loop.run_until_complete(cache.set('users', users))
    uvicorn.run('Server:app', port=5002)