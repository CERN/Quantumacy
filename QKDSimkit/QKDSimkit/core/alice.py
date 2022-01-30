# -*- coding: utf-8 -*-
# This code is part of QKDSimkit.
#
# SPDX-License-Identifier: MIT
#
# (C) Copyright 2021 CERN.

"""This module simulates Alice's operations"""

import logging
import sys

from base64 import urlsafe_b64encode

from QKDSimkit.core.qexceptions import qsocketerror, aliceerror
from QKDSimkit.core.sender import Sender

logger = logging.getLogger("QKDSimkit_logger")


def import_key(channel_address: str, ID: str, size: int = 256):
    """Alice's procedure to agree on a shared key

    Args:
        channel_address (str): channel address
        ID (str): identifier of alice-bob pair
        size (int): size of key in bits
    """
    channelIP, channelPort = channel_address.split(':')
    channelPort = int(channelPort)

    for count in range(0, 1000):
        alice = Sender(ID, size)
        try:
            # connect to quantum channel
            alice.connect_to_channel(channelIP, channelPort)
            # create and send a photon pulse through the quantum channel
            photon_pulse = alice.create_photon_pulse()
            alice.send_photon_pulse(photon_pulse)
        except qsocketerror as err:
            raise aliceerror("Connection error while connecting to the quantum channel (" + str(err) + "). Disconnecting.")
        except Exception as e:
            raise aliceerror('Generic error during qunatum photon exchange: ' + str(e))

        # connect to classic channel
        try:
            alice.reset_socket()
            alice.connect_to_channel(channelIP, channelPort)
        except qsocketerror as err:
            raise aliceerror("Connection error while connecting to the classic channel (" + str(err) + "). Disconnecting.")

        # exchange basis
        try:
            # listen for Bob's basis
            alice.listen_for('bob', 'other_bases')
            # generate the reconciled key from Bob's basis
            alice.generate_reconciled_key()
            # create and send the basis through the classic channel
            alice.send('alice-reconciled_key', repr(alice.reconciled_key))
        except qsocketerror as err:
            raise aliceerror("Connection error while exchanging bases (" + str(err) + "). Disconnecting.")
        except Exception as err:
            raise aliceerror("Generic error while exchanging bases: " + str(err))

        # create key and public sub key
        alice.create_keys()

        # exchange sub key
        try:
            # send the public sub key
            alice.send('alice-other_sub_key', repr(alice.sub_shared_key))
            # listen for Bob's public sub key
            alice.listen_for('bob', 'other_sub_key')

            alice.decision = alice.validate()

            # send decision
            alice.send('alice-other_decision', repr(alice.decision))
            # listen for Alice's sub key
            alice.listen_for('bob', 'other_decision')
        except qsocketerror as err:
            raise aliceerror("Connection error while comparing sub_keys (" + str(err) + "). Disconnecting.")
        except Exception as err:
            raise aliceerror("Generic error while comparing sub_keys (" + str(err) + "). Disconnecting.")


        alice.reset_socket()

        # choose what to do
        if alice.decision == alice.other_decision and alice.decision == 1:
            # return a correct key
            alice.get_key()
            logger.info("Success!")
            alice.key = alice.key[:size]
            alice.key = [int("".join(map(str, alice.key[i:i + 8])), 2) for i in range(0, len(alice.key), 8)]
            return urlsafe_b64encode(bytearray(alice.key))
        elif alice.decision == alice.other_decision and alice.decision == 0:
            # retry
            logger.warning("Failed to match key, trying again")
            continue
        else:
            # exit
            raise aliceerror("Failed! Noise or eavesdropper detected")
    raise aliceerror("Error: too many attempts to find a shared key")


if __name__ == '__main__':
    try:
        import_key('127.0.0.1:8000', 'id', 256)
    except aliceerror as ae:
        logger.error(str(ae))
