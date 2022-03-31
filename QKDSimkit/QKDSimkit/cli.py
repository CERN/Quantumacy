#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This code is part of QKDSimkit.
#
# SPDX-License-Identifier: MIT
#
# (C) Copyright 2021 CERN.

"""This module contains the command line interface"""

import argparse
import asyncio
import logging.config
from QKDSimkit import LOGGING

logging.config.dictConfig(LOGGING)

from QKDSimkit.Channel import start_channel
from QKDSimkit.Client import start_client
from QKDSimkit.p2p_servers import start_p2p
from QKDSimkit.Server import start_server, start_server_and_channel, get_key_cli, add_user


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
    channels = server.add_subparsers(title='Action', dest='action',
                                     help='Choose a possible action')
    parser_k = channels.add_parser('retrieve', help="Retrieve keys")
    parser_k.add_argument('-t', '--token', type=str, default=None,
                          help='Specify an identifier to retrieve a specific set of keys')
    parser_u = channels.add_parser('add_user', help='Register a new user with a token')
    parser_u.add_argument('token', help='Specify a token to identify a client')
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
    client.add_argument('-t', '--token', default='token', help='Specify token')
    client.add_argument('-k', '--show_keys', default=False, type=bool, help='Show keys in output')

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
        if args.action == 'retrieve':
            get_key_cli(args.identifier)
        if args.action == 'add_user':
            asyncio.run(add_user(args.token))
        if args.action == 'local':
            start_server_and_channel(args.channel_address, args.noise, args.eve, args.address)
        if args.action == 'external':
            start_server(args.channel_address, args.address)
    elif args.program == 'client':
        start_client(args.alice_address, args.channel_address, args.number, args.size, args.token, args.show_keys)
    elif args.program == 'channel':
        start_channel(args.address, args.noise, args.eve)
    elif args.program == 'p2p':
        start_p2p(args.node, args.address, args.channel_address)
    else:
        parser.print_help()


if __name__ == '__main__':
    cli()
