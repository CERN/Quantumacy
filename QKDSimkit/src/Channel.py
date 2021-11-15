# -*- coding: utf-8 -*-
"""
Created on Wed May 12 21:31:42 2021

@author: Alberto Di Meglio
"""

import os
import argparse
import core


def run_channel(host: str = '', port: str = '5000', noise: float = 0.0, eve: bool = False):
    # clean up
    _ = os.system('clear')

    # instantiate a receiver channel
    theChannel = core.channel.public_channel(host, port, noise, eve)

    # initiate the channel and listen for connections
    theChannel.initiate_channel()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Channel for Quantumacy')
    parser.add_argument('--host', default='', type=str,
                        help='Bind socket to this host (default: %(default)s)')
    parser.add_argument('--port', default='5000', type=str,
                        help='Bind socket to this port (default: %(default)s)')
    parser.add_argument('-n', '--noise', default=0.0, type=float,
                        help='Set a noise value for channel, type a float number in [0,1] (default: %(default)s)')
    parser.add_argument('-e', '--eve', action='store_true', help='Add an eavesdropper to the channel')
    args = parser.parse_args()
    run_channel(args.host, args.port, args.noise, args.eve)
