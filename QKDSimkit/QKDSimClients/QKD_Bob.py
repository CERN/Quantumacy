# -*- coding: utf-8 -*-
"""
Created on Wed May 12 21:57:13 2021

@author: Alberto Di Meglio
"""

import os
import sys
import json
import logging
from fastapi import FastAPI
from receiver import receiver
from qexceptions import qsocketerror
from pydantic import BaseModel


logging.basicConfig(level=logging.ERROR)


def import_key(ID: str, token: str, size: int = 512):
    s = json.load(open('../config.json', ))['channel']

    channelIP = s['host']
    channelPort = s['port']

    # clean up
    _ = os.system('clear')

    for count in range(0, 1000):
        bob = receiver(ID, token, size)

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
            return bob.key[:size]
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


if __name__ == '__main__':
    import_key('', b'7KHuKtJ1ZsV21DknPbcsOZIXfmH1_MnKdOIGymsQ5aA=')

app = FastAPI()


class qkdParams(BaseModel):
    number: int = 1
    size: int = 1024


# @app.get("/api/v1/keys/QKD_Bob/enc_keys")
@app.get("/test")
async def root(number: int = 1, size: int = 1024):
    answer = {}
    keys = []
    for i in range(0, number):
        key = import_key('', b'7KHuKtJ1ZsV21DknPbcsOZIXfmH1_MnKdOIGymsQ5aA=', size=size)
        keys.append({"key_ID": 1, "key": key})
    answer["keys"] = keys
    return answer


@app.post("/test")
async def root(qkdParams: qkdParams):
    answer = {}
    keys = []
    for i in range(0, qkdParams.number):
        key = import_key('', b'7KHuKtJ1ZsV21DknPbcsOZIXfmH1_MnKdOIGymsQ5aA=', size=qkdParams.size)
        keys.append({"key_ID": 1, "key": key})
    answer["keys"] = keys
    return answer
