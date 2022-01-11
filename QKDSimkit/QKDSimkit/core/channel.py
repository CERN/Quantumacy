# -*- coding: utf-8 -*-
# This code is part of QKDSimkit.
#
# SPDX-License-Identifier: MIT
#
# (C) Copyright 2021 CERN.

"""This module simulates channel's operations"""

import socket
import logging

from threading import Thread

from .channel_features import eavesdropper, random_errors
from .qexceptions import qsocketerror

logger = logging.getLogger("QKDSimkit_logger")


class public_channel(object):  # insecure public classical/quantum channel
    def __init__(self, address: str, noise: float, eve: bool):
        self.host = address.split(':')[0]
        self.port = address.split(':')[1]
        self.noise = noise
        self.eve = eve
        self.buffer_size = 8192
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # reusable socket
        self.ip_list = []  # blacklist already created connections
        self.conn_list = []
        self.full_data = []

    def initiate_channel(self, *port):
        """Start channel"""
        if len(port) > 0:
            self.port = str(port[0])
        if isinstance(self.port, str):
            self.port = int(self.port)

        try:
            self.socket.bind((self.host, self.port))
        except socket.error:
            raise qsocketerror("port {0} is occupied".format(self.port))

        self.socket.listen(1)

        logger.info("initiated the channel on {0}:{1}, waiting for clients...".format(self.host, self.port))

        while True:
            conn, addr = self.socket.accept()  # initiate new serving thread for every new connection:
            if conn not in self.conn_list:
                logger.info("{0} has connected.".format(addr))
                self.ip_list.append(addr)
                self.conn_list.append(conn)
                _thread = Thread(target=self.initiate_connection, args=(conn, addr))
                _thread.daemon = True
                _thread.start()
            else:
                logger.info(self.ip_list)

    def initiate_connection(self, conn, addr):
        """Listen for messages and broadcast them"""
        while True:
            try:
                data = conn.recv(self.buffer_size)
                message = data.decode()
                if len(message.split(':')) > 1:
                    if message.split(':')[1] == 'qpulse' and message.split(':')[2] != 'ack':
                        if self.eve:
                            message = eavesdropper(message.split(':', 2))
                        if self.noise > 0:
                            message = random_errors(message.split(':', 2), self.noise)
            except ConnectionResetError:
                break
            except ConnectionAbortedError:
                break

            if not message:
                break
            else:
                fwdMessage = "{0}:{1}".format(addr, message)
                logger.info(fwdMessage)
                for clients in self.conn_list:
                    try:
                        if clients.getpeername() != addr:
                            clients.sendall(fwdMessage.encode())
                    except OSError:
                        # old connections?
                        logger.warning("Ünknown connection, ignoring...")

        conn.close()
        self.conn_list.remove(conn)
        self.ip_list.remove(addr)

        logger.info(str(addr) + " has disconnected")
