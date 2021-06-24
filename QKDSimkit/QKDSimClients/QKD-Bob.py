# -*- coding: utf-8 -*-
"""
Created on Wed May 12 21:57:13 2021

@author: Alberto Di Meglio
"""

import os
import sys
import time
from receiver import receiver
from qexceptions import qsocketerror

channelIP = "192.168.1.2"
channelPort = 5005

# clean up
_ = os.system('cls')

# Bob starts listening to the quantum channel
bob = receiver()

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
    time.sleep(1)
    bob.send_classical_bits('basis', bob.basis)

    # listen for Alice's reconciled key through classic channel
    bob.listen_for_rec_key()

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
    bob.listen_for_key()

    # send the public sub key
    time.sleep(1)
    bob.send_classical_bits('key', bob.sub_shared_key)

    if bob.validate():
        decision = 1
    else:
        decision = 0

    # listen for Alice's sub key
    bob.listen_for_decision()

    # send decision
    time.sleep(1)
    bob.send_classical_bits('decision', bob.decision)

except qsocketerror as err:
    print("An error occurred while connecting to the classic channel (" + str(err) + "). Disconnecting.")
    sys.exit()
except Exception as err: 
    print("An error occurred (" + str(err) + "). Disconnecting.")
    sys.exit()

if (bob.decision == bob.other_decision):
    print("Success!")
else:
    print("Failed!")
