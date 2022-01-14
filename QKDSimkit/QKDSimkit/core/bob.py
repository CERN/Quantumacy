# -*- coding: utf-8 -*-
# This code is part of QKDSimkit.
#
# SPDX-License-Identifier: MIT
#
# (C) Copyright 2021 CERN.

"""This module simulates Bob's operations"""

import sys
import logging

from base64 import urlsafe_b64encode

from QKDSimkit.core.receiver import Receiver
from QKDSimkit.core.qexceptions import qsocketerror, boberror

logger = logging.getLogger("QKDSimkit_logger")


def import_key(channel_address: str, ID: str, size: int = 256):
    """Bob's procedure to agree on a shared key

    Args:
        channel_address (str): channel address
        ID (str): identifier of alice-bob pair
        size (int): size of key in bits
    """
    channelIP, channelPort = channel_address.split(':')
    channelPort = int(channelPort)

    for count in range(0, 1000):
        bob = Receiver(ID, size)

        try:
            # connect to channel
            bob.connect_to_channel(channelIP, channelPort)
            # listen for a photon pulse on the quantum channel (this calls is blocking)
            bob.listen_quantum()
            bob.measure_photon_pulse()
        except qsocketerror as err:
            raise boberror("Connection error while connecting to the quantum channel (" + str(err) + "). Disconnecting.")
        except Exception as e:
            raise boberror('Generic error during qunatum photon exchange: ' + str(e))

# now connect to classic channel
        try:
            # connect to channel
            bob.reset_socket()
            bob.connect_to_channel(channelIP, channelPort)
        except qsocketerror as err:
            raise boberror(
                "Connection error while connecting to the classic channel (" + str(err) + "). Disconnecting.")

        # exchange basis
        try:
            # send Bob's chosen basis
            bob.send('bob-other_bases', repr(bob.bases))
            # listen for Alice's reconciled key through classic channel
            bob.listen_for('alice', 'reconciled_key')
        except qsocketerror as err:
            raise boberror("Connection error while exchanging bases (" + str(err) + "). Disconnecting.")
        except Exception as err:
            raise boberror("Generic error while exchanging bases: " + str(err))

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
            raise boberror("Connection error while comparing sub_keys (" + str(err) + "). Disconnecting.")
        except Exception as err:
            raise boberror("Generic error while comparing sub_keys (" + str(err) + "). Disconnecting.")

        bob.reset_socket()

        # choose what to do
        if bob.decision == bob.other_decision and bob.decision == 1:
            # return a correct key
            bob.get_key()
            logger.info("Success!")
            bob.key = bob.key[:size]
            bob.key = [int("".join(map(str, bob.key[i:i + 8])), 2) for i in range(0, len(bob.key), 8)]
            return urlsafe_b64encode(bytearray(bob.key))
        elif bob.decision == bob.other_decision and bob.decision == 0:
            # retry
            logger.info("Failed to match key, trying again")
            continue
        else:
            # exit
            raise boberror("Failed! Noise or eavesdropper detected")
    raise boberror("Error: too many attempts to find a shared key")


if __name__ == '__main__':
    try:
        import_key('127.0.0.1:8000', 'id', 256)
    except boberror as be:
        logger.error(str(be))
