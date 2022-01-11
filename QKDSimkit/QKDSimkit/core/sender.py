# -*- coding: utf-8 -*-
# This code is part of QKDSimkit.
#
# SPDX-License-Identifier: MIT
#
# (C) Copyright 2021 CERN.

import logging
import socket
import sys

from .models import Photon
from .node import Node
from .qexceptions import qsocketerror, qobjecterror

logger = logging.getLogger("QKDSimkit_logger")

class Sender(Node):
    """Sender class, it expands Node, it contains methods to communicate a receiver node, the general idea is that this
    node dictate the communication and the receiver can just answer"""

    def __init__(self, ID, size: int):
        super().__init__(ID, size)

    def create_photon_pulse(self) -> list:
        """Create a list of photons given a size
        Returns:
             list of photons"""
        for i in range(self.photon_pulse_size):
            self.photon_pulse.append(Photon())
        self.bases = [p.basis for p in self.photon_pulse]
        return self.photon_pulse

    def send_photon_pulse(self, pulse: list):
        """Send an already created photon pulse
        it takes the polarization from each photon

        Args:
            pulse (list): photon pulse to be sent
        """
        if not isinstance(pulse, list):
            raise qobjecterror("argument must be list")
        try:
            message = ''
            for p in range(len(pulse)):
                message += str(pulse[p].polarization) + "~"
            self.send("qpulse", message)
        except socket.error:
            raise qsocketerror("not connected to any channel")

    def generate_reconciled_key(self):
        """Generate a common key between the two parties

        it checks for every photon if the chosen basis is common, if it is not common the basis is discarded
        """
        if len(self.bases) != len(self.other_bases):
            raise qobjecterror("both pulses must contain the same amount of photons")
        else:
            for i in range(len(self.bases)):
                if self.bases[i] == self.other_bases[i]:
                    self.reconciled_key.append(self.bases[i])
                else:
                    self.reconciled_key.append("")

    def send(self, header: str, message: str):
        """Sender method for sender node
        it sends a message and wait for an acknowledgment if it doesn't receive the ack in the given time
        timeout_in_seconds it may try multiple times depending on the variable connection_attempts

        Args:
            header (str): unique identifier
            message (str): string to be sent
        """
        try:
            data = header + ':' + message + ':'
            to_be_sent = (self.ID + ':' + data).encode()
            for i in range(self.connection_attempts):
                self.socket.send(to_be_sent)
                logger.info('Sent: ' + header + ':' + message)
                received = self.recv_all()
                if not received:
                    continue
                if received[0] == header and received[1] == 'ack':
                    return
            raise ConnectionError
        except Exception as err:
            logger.error('Alice failed to send {0}:\n{1}'.format(header, str(err)))
            sys.exit()
        except ConnectionError as e:
            logger.error('Alice tried to receive too many times \n' + str(e))
            sys.exit()

    def recv(self, header: str):
        """Receiver method for sender node
        It will send a request message with the given header and it will wait for the response for a time
        timeout_in_seconds it may try multiple times depending on the variable connection_attempts, every received
        message with a different header will be discarded

        Args:
            header (str): unique identifier
        """
        try:
            for i in range(self.connection_attempts):
                to_be_sent = (self.ID + ':' + header + ':request:').encode()
                self.socket.send(to_be_sent)
                received = self.recv_all()
                if not received:
                    continue
                if received[0] == header:
                    dec_message = received[1]
                    logger.info("Received: " + header + ":" + dec_message)
                    return dec_message
            raise ConnectionError
        except ConnectionError:
            raise qsocketerror("Alice tried to receive too many times ")

