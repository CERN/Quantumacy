# -*- coding: utf-8 -*-
"""
Created on Wed May 12 21:57:13 2021

@author: Alberto Di Meglio
"""

import os
import sys
import json
import logging
from sender import sender
from qexceptions import qsocketerror, qobjecterror


def import_key():
    c = json.load(open('../config.json', ))['channel']
    channelIP = c['host']
    channelPort = c['port']

    # clean up
    _ = os.system('clear')

    for count in range(0, 1000):
        alice = sender()
        try:
            # connect to quantum channel
            alice.connect_to_channel(channelIP, channelPort)
            # create and send a photon pulse through the quantum channel
            photon_pulse = alice.create_photon_pulse()
            alice.send_photon_pulse(photon_pulse)

        except qsocketerror as err:
            logging.error("An error occurred while connecting to the quantum channel (" + str(err) + "). Disconnecting.")
            sys.exit()
        except Exception as e:
            logging.error("An error occurred. Disconnecting.\n" + str(e))
            sys.exit()

        # connect to classic channel
        try:
            alice.reset_socket()
            alice.connect_to_channel(channelIP, channelPort)
        except qsocketerror as err:
            logging.error("An error occurred while connecting to the classic channel (" + str(err) + "). Disconnecting.")
            sys.exit()
        except Exception as err:
            logging.error("An error occurred (" + str(err) + "). Disconnecting.")
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
            logging.error("An error occurred while connecting to the classic channel (" + str(err) + "). Disconnecting.")
            sys.exit()
        except Exception as err:
            logging.error("An error occurred (" + str(err) + "). Disconnecting.")
            sys.exit()

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
            logging.error("An error occurred while connecting to the classic channel (" + str(err) + "). Disconnecting.")
            sys.exit()
        except Exception as err:
            logging.error("An error occurred (" + str(err) + "). Disconnecting.")
            sys.exit()

        alice.reset_socket()

        # choose what to do
        if alice.decision == alice.other_decision and alice.decision == 1:
            #return a correct key
            alice.get_key()
            logging.info("Success!")
            return alice.key
        elif alice.decision == alice.other_decision and alice.decision == 0:
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
    print(len(import_key()))
    print(import_key())
