# -*- coding: utf-8 -*-
"""
Created on Wed May 12 21:57:13 2021

@author: Alberto Di Meglio
"""

import os
import sys
import json
import hashlib
import logging
from receiver import receiver
from qexceptions import qsocketerror


def import_key(count=0):
    s = json.load(open('../config.json', ))['channel']

    channelIP = s['host']
    channelPort = s['port']

    # clean up
    _ = os.system('cls')
    # Bob starts listening to the quantum channel
    bob = receiver()

    if count >= bob.max_repetitions:
        print("Error: too many attempts to find a shared key")
        return -1

    try:
        # connect to channel
        bob.connect_to_channel(channelIP, channelPort)
        # listen for a photon pulse on the quantum channel (this calls is blocking)
        bob.listen_quantum()
        bob.measure_photon_pulse()

    except qsocketerror as err:
        print("An error occurred while connecting to the quantum channel (" + str(err) + "). Disconnecting.")
        sys.exit()
    except Exception as err:
        print("An error occurred (" + str(err) + "). Disconnecting.")
        sys.exit()

    # now connect to classic channel
    try:
        # connect to channel
        bob.reset_socket()
        bob.connect_to_channel(channelIP, channelPort)
    except qsocketerror as err:
        print("An error occurred while connecting to the classic channel (" + str(err) + "). Disconnecting.")
        sys.exit()
    except Exception as err:
        print("An error occurred (" + str(err) + "). Disconnecting.")
        sys.exit()

    # exchange basis
    try:
        # send Bob's chosen basis
        bob.send('bob-other_basis', repr(bob.basis))
        # listen for Alice's reconciled key through classic channel
        bob.listen_for('alice', 'reconciled_key')

    except qsocketerror as err:
        print("An error occurred while connecting to the classic channel (" + str(err) + "). Disconnecting.")
        sys.exit()
    except Exception as err:
        print("An error occurred (" + str(err) + "). Disconnecting.")
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
        print("An error occurred while connecting to the classic channel (" + str(err) + "). Disconnecting.")
        sys.exit()
    except Exception as err:
        print("An error occurred (" + str(err) + "). Disconnecting.")
        sys.exit()

    bob.reset_socket()

    if bob.decision == bob.other_decision and bob.decision == 1:
        bob.get_key()
        print("Success!")
    elif bob.decision == bob.other_decision and bob.decision == 0:
        return import_key(count + 1)
    else:
        print("Failed! Noise or eavesdropper detected")
        return -1

    return bob.key


if __name__ == '__main__':
    print(import_key())
