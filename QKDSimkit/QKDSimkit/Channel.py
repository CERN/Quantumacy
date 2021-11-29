#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This code is part of QKDSimkit.
#
# SPDX-License-Identifier: MIT
#
# (C) Copyright 2021 CERN.

import argparse

from QKDSimkit.core import channel


def start_channel(address, noise, eve):

    # instantiate a receiver channel
    theChannel = channel.public_channel(address, noise, eve)

    # initiate the channel and listen for connections
    theChannel.initiate_channel()


def manage_args():
    parser = argparse.ArgumentParser(description='Channel for Quantumacy')
    parser.add_argument('-a', '--address', default=':5000', type=str,
                        help='Bind socket to this address (default: %(default)s)')
    parser.add_argument('-n', '--noise', default=0.0, type=float,
                        help='Set a noise value for channel, type a float number in [0,1] (default: %(default)s)')
    parser.add_argument('-e', '--eve', action='store_true', help='Add an eavesdropper to the channel')
    return parser


if __name__ == '__main__':
    args = manage_args().parse_args()
    start_channel(args.address, args.noise, args.eve)