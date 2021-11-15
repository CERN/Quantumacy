import uvicorn
import json
import logging
import argparse
import core
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


logging.basicConfig(level=logging.ERROR)

alice_app = FastAPI()
bob_app = FastAPI()


class qkdParams(BaseModel):
    number: int = 1
    size: int = 256
    ID: str = 'id'


def answer_get(number, size, ID, type):
    answer = {}
    keys = []
    s = json.load(open('../data/config.json', ))['channel']
    address = '{}:{}'.format(s['host'], s['port'])
    for i in range(number):
        if type == 'Alice':
            key = core.alice.import_key(channel_address=address, ID=ID, size=size)
        if type == 'Bob':
            key = core.bob.import_key(channel_address=address, ID=ID, size=size)
        keys.append({"key_ID": i, "key": key})
    answer["keys"] = keys
    return answer


@alice_app.get("/test")
async def root(number: int = 1, size: int = 256, ID: str = 'id'):
    return answer_get(number, size, ID, 'Alice')


@bob_app.get("/test")
async def root(number: int = 1, size: int = 256, ID: str = 'id'):
    return answer_get(number, size, ID, 'Bob')


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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Server for Quantumacy')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-a', '--sender', action='store_const', dest='node', const='alice',
                       help='Run this server as a sender (Alice) node')
    group.add_argument('-b', '--receiver', action='store_const', dest='node', const='bob',
                       help='Run this server as a receiver (Bob) node')
    parser.add_argument('-c', '--channel', default=':5000', type=str,
                        help='Specify the address of the channel [host:port]')
    a = parser.parse_args()
    uvicorn.run('p2p_servers:{}_app'.format(a.node), port=5003)
