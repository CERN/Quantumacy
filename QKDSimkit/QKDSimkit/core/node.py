# -*- coding: utf-8 -*-
# This code is part of QKDSimkit.
#
# SPDX-License-Identifier: MIT
#
# (C) Copyright 2021 CERN.

import abc
import ast
import logging
import re
import select
import socket

from .qexceptions import qsocketerror
from .utils import validate

MIN_SHARED = 20
BUFFER_SIZE = 8192
TIMEOUT_IN_SECONDS = 1
CONNECTION_ATTEMPTS = 60
MAX_REPETITIONS = 1000
MIN_SHARED_PERCENT = 0.89

logger = logging.getLogger("QKDSimkit_logger")


class Node(object):
    """Father class for receiver and sender

    Args:
        ID (str): identifier of alice-bob pair
        size (int): size of key in bits

    Attributes:
        min_shared (int): 
        buffer_size (int):
        timeout_in_seconds (int):
        connection_attempts (int):
        max_repetitions (int):
        min_shared_percent (float):
        socket: socket
        ID (str): identifier of alice-bob pair
        photon_pulse (list): list of photons
        bases (list): list of bases
        other_bases (list): list of bases of the other node
        reconciled_key (list): key with only common values and ""
        shared_key (list): key with only common values
        sub_shared_key (list): first half of the key
        other_sub_key (list): first half of the key of the other node
        decision (int): result of comparison between shared part of the key
        other_decision (int): result of comparison between ke ys
        not_shared_key (list):
        key (list): non-revealed part of the key
        fragments (list):
        regex: utility regex
        photon_pulse_size (int): number of photons exchanged photons
    """
    def __init__(self, ID, size):
        self.min_shared = MIN_SHARED
        self.buffer_size = BUFFER_SIZE
        self.timeout_in_seconds = TIMEOUT_IN_SECONDS
        self.connection_attempts = CONNECTION_ATTEMPTS
        self.max_repetitions = MAX_REPETITIONS
        self.min_shared_percent = MIN_SHARED_PERCENT
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ID = ID
        self.photon_pulse = []
        self.bases = []
        self.other_bases = []
        self.reconciled_key = []
        self.shared_key = []
        self.sub_shared_key = []
        self.other_sub_key = []
        self.decision = 0
        self.other_decision = 0
        self.key = []
        self.regex = r'\((.)*\):'
        self.photon_pulse_size = size * 5

    def connect_to_channel(self, address: str, port: int):
        """It starts the connection with the channel

        Args:
            address (str): address
            port (int): port

        """
        try:
            self.socket.connect((address, port))
        except socket.error:
            raise qsocketerror("unable to connect")

    def reset_socket(self):
        """Reset the previously started socket
        """
        try:
            self.socket.close()
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except Exception as e:
            logger.info("Failed to reset socket:\n" + str(e))
            raise qsocketerror

    def ownMessage(self, addr: str) -> bool:
        """Check if a message comes from this node

        Args:
            addr (str): address of the received message
        """
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        if local_ip == addr:
            return True
        return False

    def create_keys(self):
        """It calls two functions to elaborate th photon pulse in actual keys"""
        self.create_shared_key()
        self.create_sub_shared_key()

    def create_shared_key(self):
        """Converts the whole photon pulse in a list of bit"""
        for i in range(len(self.photon_pulse)):
            if self.reconciled_key[i] != "":
                self.shared_key.append(self.photon_pulse[i].bit)

    def create_sub_shared_key(self):
        """Create the part of the key that will be sent to the other node (first half)"""
        self.sub_shared_key = self.shared_key[:(len(self.shared_key) // 2)]

    def get_key(self):
        """Create the part of the key that will not be sent and it will be used as symmetric key (second half)"""
        self.key = self.shared_key[(len(self.shared_key) // 2):]

    def listen_for(self, sender: str, attr: str):
        """Receive a message and store it in the right place

        Args:
            sender (str): name of the node from which we expect to receive
            attr (str): name of the attribute that will store the content of the received message
            """
        try:
            logger.info("Listening to classical channel for " + attr)
            while True:
                message = self.recv(sender + '-' + attr)
                try:
                    literal = ast.literal_eval(message)
                except ValueError as VE:
                    logger.error("Value Error: " + str(VE))
                    pass
                else:
                    setattr(self, attr, literal)
                    break
        except socket.error:
            raise qsocketerror("not connected to any channel")

    def validate(self) -> int:
        """Wrapper of utils.validate it manages different outputs, it also gives info of eventual errors

        Returns:
            int: 1: keys are equals, 0: error rate is below a given percent, -1: error rate too high
        """
        percent = validate(self.sub_shared_key, self.other_sub_key)
        logger.info('Correct bits percentage: ' + str(percent))
        if percent == 1:
            return 1
        if self.min_shared_percent <= percent < 1:
            return 0
        if percent < self.min_shared_percent:
            return -1

    def recv_all(self) -> list:
        """receive a message
        receive from socket, sum every part of the message, check if the message is commplete, check if the ID of the
        sender corresponds to the ID of the receiver, return a list whit header and payload, please note that the ID
        is not returned

        Returns:
            fragments (list): list made by header and payload
        """
        message = ''
        ready = select.select([self.socket], [], [], self.timeout_in_seconds)
        if ready[0]:
            while True:
                data_recv = self.socket.recv(self.buffer_size).decode()
                message += re.sub(self.regex, '', data_recv)  # removing ('xxx.xxx.xxx.xxx', xxxxx):
                if message.count(':') >= 3:  # checking if payload started and finished example: 'ID:head:payload:'
                    fragments = message.split(':', 3)
                    if fragments[0] != self.ID:  # this message doesn't belong to this node
                        message = fragments[3]  # we can discard it
                        continue
                    else:
                        return fragments[1:]  # we don't need to return ID because we already checked it is correct

    @abc.abstractmethod
    def send(self, header: str, message: str):
        """abstract method"""
        print("send(): Override me")

    @abc.abstractmethod
    def recv(self, header: str):
        """abstract method"""
        print("receive(): Override me")
