# -*- coding: utf-8 -*-
"""
Created on Wed May 12 21:57:13 2021

@author: Alberto Di Meglio
"""

import os
import sys
import json
import logging
import uvicorn
from base64 import urlsafe_b64encode
from fastapi import FastAPI
from QKDSimkit.QKDSimClients.receiver import receiver
from QKDSimkit.QKDSimChannels.qexceptions import qsocketerror
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


logging.basicConfig(level=logging.ERROR)

app = FastAPI()


def import_key(channel_address: str, ID: str, size: int = 256):

    channelIP, channelPort = channel_address.split(':')
    channelPort = int(channelPort)

    # clean up
    _ = os.system('clear')

    for count in range(0, 1000):
        bob = receiver(ID, size)

        try:
            # connect to channel
            bob.connect_to_channel(channelIP, channelPort)
            # listen for a photon pulse on the quantum channel (this calls is blocking)
            bob.listen_quantum()
            bob.measure_photon_pulse()

        except qsocketerror as err:
            logging.error(
                "An error occurred while connecting to the quantum channel (" + str(err) + "). Disconnecting.")
            sys.exit()
        except Exception as err:
            logging.error("An error occurred (" + str(err) + "). Disconnecting.")
            sys.exit()

        # now connect to classic channel
        try:
            # connect to channel
            bob.reset_socket()
            bob.connect_to_channel(channelIP, channelPort)
        except qsocketerror as err:
            logging.error(
                "An error occurred while connecting to the classic channel (" + str(err) + "). Disconnecting.")
            sys.exit()
        except Exception as err:
            logging.error("An error occurred (" + str(err) + "). Disconnecting.")
            sys.exit()

        # exchange basis
        try:
            # send Bob's chosen basis
            bob.send('bob-other_basis', repr(bob.basis))
            # listen for Alice's reconciled key through classic channel
            bob.listen_for('alice', 'reconciled_key')

        except qsocketerror as err:
            logging.error(
                "An error occurred while connecting to the classic channel (" + str(err) + "). Disconnecting.")
            sys.exit()
        except Exception as err:
            logging.error("An error occurred (" + str(err) + "). Disconnecting.")
            sys.exit()

        # create key and public sub key
        bob.create_keys()

        # exchange sub key
        try:
            # listen for Alice's sub key
            bob.listen_for('alice', 'other_sub_key')

            # send the public sub key
            bob.send('bob-other_sub_key', repr(bob.sub_shared_key))

            bob.decision = bob.validate()

            # listen for Alice's sub key
            bob.listen_for('alice', 'other_decision')

            # send decision
            bob.send('bob-other_decision', repr(bob.decision))

        except qsocketerror as err:
            logging.error(
                "An error occurred while connecting to the classic channel (" + str(err) + "). Disconnecting.")
            sys.exit()
        except Exception as err:
            logging.error("An error occurred (" + str(err) + "). Disconnecting.")
            sys.exit()

        bob.reset_socket()

        # choose what to do
        if bob.decision == bob.other_decision and bob.decision == 1:
            # return a correct key
            bob.get_key()
            logging.info("Success!")
            bob.key = bob.key[:size]
            bob.key = [int("".join(map(str, bob.key[i:i + 8])), 2) for i in range(0, len(bob.key), 8)]
            return urlsafe_b64encode(bytearray(bob.key))
        elif bob.decision == bob.other_decision and bob.decision == 0:
            # retry
            logging.info("Failed to match key, trying again")
            continue
        else:
            # exit
            logging.warning("Failed! Noise or eavesdropper detected")
            return -1
    logging.warning("Error: too many attempts to find a shared key")
    return -1


class qkdParams(BaseModel):
    number: int = 1
    size: int = 256
    ID: str = 'id'


@app.get("/test")
async def root(number: int = 1, size: int = 256, ID: str = 'id'):
    answer = {}
    keys = []
    s = json.load(open('../config.json', ))['channel']
    address = '{}:{}'.format(s['host'], s['port'])
    for i in range(number):
        key = import_key(channel_address=address, ID=ID, size=size)
        keys.append({"key_ID": i, "key": key})
    answer["keys"] = keys
    return answer


@app.post("/test")
async def root(qkdParams: qkdParams):
    answer = {}
    keys = []
    for i in range(qkdParams.number):
        key = import_key(qkdParams.ID, size=qkdParams.size)
        keys.append({"key_ID": i, "key": key})
    answer["keys"] = keys
    return answer

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


if __name__ == '__main__':
    #TODO: fix this to provide different options and update token management
    uvicorn.run('QKD_Bob:app', port=5003)

#    import_key('id', b'7KHuKtJ1ZsV21DknPbcsOZIXfmH1_MnKdOIGymsQ5aA=')
