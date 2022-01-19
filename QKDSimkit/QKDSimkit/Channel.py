#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This code is part of QKDSimkit.
#
# SPDX-License-Identifier: MIT
#
# (C) Copyright 2021 CERN.

"""This module contains channel's interface"""

import argparse
import logging
import sys

from QKDSimkit.core import channel
from QKDSimkit.core.qexceptions import qsocketerror
from QKDSimkit.core.qexceptions import qnoiseerror

logger = logging.getLogger("QKDSimkit")


def start_channel(address: str, noise: float, eve: bool):
    """Starts channel
    Args:
        address (str): where to bind the channel
        noise (float): ratio of noise in channel
        eve (bool): simulate an eavesdropper in channel
    """
    # instantiate a receiver channel
    theChannel = channel.public_channel(address, noise, eve)
    try:
        # initiate the channel and listen for connections
        theChannel.initiate_channel()
    except qsocketerror as qs:
        logger.error(str(qs))
        sys.exit()
    except qnoiseerror as qn:
        logger.error(str(qn))
        sys.exit()


def manage_args():
    """Manages possible arguments and provides help messages"""

    parser = argparse.ArgumentParser(description='Channel for Quantumacy')
    parser.add_argument('-a', '--address', default=':8000', type=str,
                        help='Bind socket to this address (default: %(default)s)')
    parser.add_argument('-n', '--noise', default=0.0, type=float,
                        help='Set a noise value for channel, type a float number in [0,1] (default: %(default)s)')
    parser.add_argument('-e', '--eve', action='store_true', help='Add an eavesdropper to the channel')
    return parser


if __name__ == '__main__':
    args = manage_args().parse_args()
    try:
        start_channel(args.address, args.noise, args.eve)
    except Exception as e:
        logger.error(str(e))
