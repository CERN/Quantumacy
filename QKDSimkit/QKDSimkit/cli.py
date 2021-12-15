#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This code is part of QKDSimkit.
#
# SPDX-License-Identifier: MIT
#
# (C) Copyright 2021 CERN.

"""This module contains the command line interface"""

import argparse

from aiocache import Cache

from QKDSimkit.Channel import start_channel
from QKDSimkit.Client import start_client
from QKDSimkit.p2p_servers import start_p2p
from QKDSimkit.Server import start_server, start_server_and_channel


def cli():
    """Command line interface
    single entry point for server, client, channel and peer to peer node"""
    parser = argparse.ArgumentParser(description='QKDSimkit interface: choose one of the following programs')
    interfaces = parser.add_subparsers(dest='program')

    #   SERVER PARSER
    #   =============

    server = interfaces.add_parser(name='server', description='Server for QKDSimkit')
    server.add_argument('-a', '--address', default='127.0.0.1:5002', type=str,
                        help='Bind socket to this address (default: %(default)s)')
    channels = server.add_subparsers(title='Channel type', dest='channel_type', required=True,
                                     help='Specify where the channel is (required)')
    parser_l = channels.add_parser('local', help='Run the channel on this machine')
    parser_l.add_argument('-ca', '--channel_address', default=':5000', type=str,
                          help='Bind socket to this address (default: %(default)s)')
    parser_l.add_argument('-n', '--noise', default=0.0, type=float,
                          help='Set a noise value for channel, type a float number in [0,1] (default: %(default)s)')
    parser_l.add_argument('-e', '--eve', action='store_true',
                          help='Add an eavesdropper to the channel')
    parser_e = channels.add_parser('external', help='Connect to an external channel')
    parser_e.add_argument('-ca', '--channel_address', type=str, required=True, help='Address of channel [host:port]')

    #   CLIENT PARSER
    #   =============

    client = interfaces.add_parser(name='client', description='Client for QKDSimkit')
    client.add_argument('alice_address', type=str, help='Address of server/Alice [host:port]')
    client.add_argument('channel_address', type=str, help='Address of channel [host:port]')
    client.add_argument('-n', '--number', default=1, type=int, help="Number of keys (default: %(default)s)")
    client.add_argument('-s', '--size', default=256, type=int, help="Size of keys (default: %(default)s)")

    #   CHANNEL PARSER
    #   ==============

    channel = interfaces.add_parser(name='channel', description='Channel for QKDSimkit')
    channel.add_argument('-a', '--address', default=':5000', type=str,
                         help='Bind socket to this address (default: %(default)s)')
    channel.add_argument('-n', '--noise', default=0.0, type=float,
                         help='Set a noise value for channel, type a float number in [0,1] (default: %(default)s)')
    channel.add_argument('-e', '--eve', action='store_true', help='Add an eavesdropper to the channel')

    #   PEER TO PEER PARSER
    #   ===================

    p2p = interfaces.add_parser(name='p2p', description='Peer to peer interface for QKDSimkit')
    p2p.add_argument('node', choices=['alice', 'bob'],
                     help='Choose how to run this node')
    p2p.add_argument('-c', '--channel_address', default=':5000', type=str,
                     help='Specify the address of the channel [host:port]')
    p2p.add_argument('-a', '--address', default='127.0.0.1:5003', type=str,
                     help='Bind socket to this address (default: %(default)s)')

    args = parser.parse_args()

    if args.program == 'server':
        if args.channel_type == 'local':
            start_server_and_channel(args.channel_address, args.noise, args.eve, args.address)
        if args.channel_type == 'external':
            start_server(args.channel_address, args.address)
    elif args.program == 'client':
        start_client(args.alice_address, args.channel_address, args.number, args.size)
    elif args.program == 'channel':
        start_channel(args.address, args.noise, args.eve)
    elif args.program == 'p2p':
        start_p2p(args.node, args.address, args.channel_address)
    else:
        parser.print_help()


if __name__ == '__main__':
    cli()
