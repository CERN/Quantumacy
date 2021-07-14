# -*- coding: utf-8 -*-
"""
Created on Wed May 12 21:57:13 2021

@author: Alberto Di Meglio
"""

import os
import sys
import json
import time
from sender import sender
from qexceptions import qsocketerror, qobjecterror


def import_key():
    s = json.load(open('../config.json', ))['channel']
    channelIP = s['host']
    channelPort = s['port']
    DEBUG = True
    # clean up
    _ = os.system('cls')

    # Alice connects to the quantum channel
    alice = sender()
    if DEBUG:
        alice.tokens.append('3c469e9d6c5875d37a43f353d4f88e61fcf812c66eee3457465a40b0da4153e0')

    try:
        alice.connect_to_channel(channelIP, channelPort)
        while not alice.authenticate():
            True
        alice.reset_socket()
    except Exception:
        print("Failed to authenticate Bob")

    try:
        # connect to quantum channel
        alice.connect_to_channel(channelIP, channelPort)
        # create and send a photon pulse through the quantum channel
        photon_pulse = alice.create_photon_pulse()
        alice.send_photon_pulse(photon_pulse)

    except qsocketerror as err:
        print("An error occurred while connecting to the quantum channel (" + str(err) + "). Disconnecting.")
        sys.exit()
    except:
        print("An error occurred. Disconnecting.")
        sys.exit()

    # connect to classic channel
    try:
        alice.reset_socket()
        alice.connect_to_channel(channelIP, channelPort)
    except qsocketerror as err:
        print("An error occurred while connecting to the classic channel (" + str(err) + "). Disconnecting.")
        sys.exit()
    except Exception as err:
        print("An error occurred (" + str(err) + "). Disconnecting.")
        sys.exit()

    # exchange basis
    try:
        # listen for Bob's basis
        alice.listen_for('bob', 'other_basis')
        # generate the reconciled key from Bob's basis
        alice.generate_reconciled_key()
        # create and send the basis through the classic channel
        alice.send('alice-reconciled_key', repr(alice.reconciled_key))

    except qsocketerror as err:
        print("An error occurred while connecting to the classic channel (" + str(err) + "). Disconnecting.")
        sys.exit()
    except Exception as err:
        print("An error occurred (" + str(err) + "). Disconnecting.")
        sys.exit()

    # create key and public sub key
    alice.create_keys()

    # exchange sub key
    try:
        # send the public sub key
        alice.send('alice-other_sub_key', repr(alice.sub_shared_key))
        # listen for Bob's public sub key
        alice.listen_for('bob', 'other_sub_key')

        if alice.validate():
            decision = 1
        else:
            decision = 0
        # send decision
        alice.send('alice-other_decision', repr(decision))
        # listen for Alice's sub key
        alice.listen_for('bob', 'other_decision')
    except qsocketerror as err:
        print("An error occurred while connecting to the classic channel (" + str(err) + "). Disconnecting.")
        sys.exit()
    except Exception as err:
        print("An error occurred (" + str(err) + "). Disconnecting.")
        sys.exit()

    if alice.decision == alice.other_decision:
        alice.importkey()
        print("Success!")
    else:
        print("Failed!")

    alice.reset_socket()

    return alice.key


if __name__ == '__main__':
    code()
