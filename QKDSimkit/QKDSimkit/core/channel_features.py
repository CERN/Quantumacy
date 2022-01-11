# -*- coding: utf-8 -*-
# This code is part of QKDSimkit.
#
# SPDX-License-Identifier: MIT
#
# (C) Copyright 2021 CERN.

"""This module contains methods to simulate some feature of a channel"""

import logging
import random
import sys

from .models import Photon
from QKDSimkit.core.qexceptions import qnoiseerror

logger = logging.getLogger("QKDSimkit_logger")


def eavesdropper(photon_stream) -> str:
    """Method to simulate an eavesdropper in a quantum channel

    Args:
        photon_stream (str): message containing polarizations
    Returns:
        message with new (eavesdropped) polarizations
    """
    try:
        photon_pulse = []
        new_message = '' + photon_stream[0] + ':' + photon_stream[1] + ':'
        polarization_vector = photon_stream[2].split("~")[:-1]
        for p in range(len(polarization_vector)):
            photon_pulse.append(Photon())
            photon_pulse[p].polarization = photon_pulse[p].measure(int(polarization_vector[p]))
            photon_pulse[p].bit = photon_pulse[p].set_bit_from_measurement()
            new_message += str(photon_pulse[p].polarization) + '~'
        return new_message + ':'
    except Exception as e:
        raise qnoiseerror('Eavesdropper error:\n' + str(e))


def random_errors(photon_stream, rate: float) -> str:
    """Method to simulate random errors in a quantum channel

    Args:
        photon_stream (str): message containing polarizations
        rate (float): decimal number from 0 to 1, it sets the error rate
    Returns:
        message with errors
    """
    try:
        polarization_vector = photon_stream[2].split("~")[:-1]
        new_message = '' + photon_stream[0] + ':' + photon_stream[1] + ':'
        count = 0
        for p in polarization_vector:
            if random.randint(1, 100) <= rate*100:
                polarization = random.randint(0, 3) * 45
                new_message += str(polarization) + '~'
                count += 1
            else:
                new_message += str(p) + '~'
        logger.info('Errors: ' + str(count))
        return new_message + ':'
    except Exception as e:
        raise qnoiseerror("Failed to add errors in photon stream:\n" + str(e))
