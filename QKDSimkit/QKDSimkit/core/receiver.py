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
from .qexceptions import qsocketerror

logger = logging.getLogger("QKDSimkit_logger")


class Receiver(Node):
    """Receiver class, it expands node, it contains methods to communicate a sender node, it can't take action but it
    has to wait for the sender node for sending data, it can answer to a request with a message or to a message with an
    acknowledgement"""
    def __init__(self, ID, size):
        super().__init__(ID, size)
        self.polarization_vector = []
        self.sent_acks = []
        self.sent_messages = {}

    def measure_photon_pulse(self):
        """Measure photon pulse

        given the vector that stores polarizations of received photons it creates a list of photons each polarization,
        basis and bit will be determined byt the measure method according to physical properties, a list with the basis
        of every photon will be stored
        """
        for p in range(len(self.polarization_vector)):
            self.photon_pulse.append(Photon())
            self.photon_pulse[p].polarization = self.photon_pulse[p].measure(int(self.polarization_vector[p]))
            self.photon_pulse[p].bit = self.photon_pulse[p].set_bit_from_measurement()
        self.bases = [p.basis for p in self.photon_pulse]

    def listen_quantum(self):
        """ Listen method to receive photon pulse
        it behaves like a wrapper for recv for photon pulses
        """
        try:
            logger.info("listening to quantum channel for photon pulse...")
            while True:
                message = self.recv('qpulse')
                self.polarization_vector = message.split("~")[:-1]
                break
        except socket.error:
            raise qsocketerror("not connected to any channel")

    def recv(self, header: str) -> str:
        """Receive function for receiver node
        it listen for a message, in case the header of the received message doesn't match it checks if an acknowledgment
        for the received message has been already sent or if the received message is an acknowledgement itself for a
        previously sent message, it sends a new acknowledgment in the first case and it sends again the message in the
        other case, if the message is new and the header is correct it sends an acknowledgement and it saves it
        Args:
            header (str): unique identifier of the message that has to be received
        Returns:
            message (str): the payload of the received data, the header and some other infos are not returned
        """
        try:
            for i in range(self.connection_attempts):  # loop for different messages
                received = self.recv_all()
                if not received:
                    continue
                label = received[0]
                if label != header and label in self.sent_acks:  # received an already received message
                    to_be_sent = (self.ID + ':' + label + ":ack:").encode()
                    self.socket.send(to_be_sent)
                    logger.info("Sent: " + label + ':ack:')
                    continue
                elif label != header and label in self.sent_messages:  # received a request for an already sent message
                    to_be_sent = (self.ID + ':' + label + ":" + self.sent_messages[label] + ':').encode()
                    self.socket.send(to_be_sent)
                    logger.info("Sent: " + label + ':' + self.sent_messages[label] + ':')
                    continue
                elif label == header:
                    dec_message = received[1]
                    to_be_sent = (self.ID + ':' + header + ":ack:").encode()
                    self.socket.send(to_be_sent)
                    self.sent_acks.append(label)
                    logger.info("Received: " + label + ":" + dec_message)
                    return dec_message
                else:
                    raise Exception
            raise ConnectionError

        except Exception as err:
            logger.error('Bob failed to receive {0}:\n{1}'.format(header, str(err)))
            sys.exit()
        except ConnectionError:
            logger.error("Bob failed to receive {0}".format(header))
            sys.exit()

    def send(self, header: str, message: str):
        """ Send method for receiver
        it listens for the request from the sender node, in case the header of the received message doesn't match it
        checks if an acknowledgment for the received header has been already sent or if the message for the requested
        header has been already sent, it sends a new acknowledgement in the first case and it sends again the message in
        the other case, it sends the expected message if the header is correct, the sent message is saved in a list
        Args:
            header (str): unique identifier
            message (str): message
        """
        try:
            for i in range(self.connection_attempts):
                received = self.recv_all()
                if not received:
                    continue
                label = received[0]
                if label != header and label in self.sent_acks:  # received an already received message
                    to_be_sent = (self.ID + ':' + label + ":ack:").encode()
                    self.socket.send(to_be_sent)
                    logger.info("Sent: " + label + ':ack:')
                    continue
                elif label != header and label in self.sent_messages:  # received a request for an already sent message
                    to_be_sent = (self.ID + ':' + label + ":" + self.sent_messages[label] + ':').encode()
                    self.socket.send(to_be_sent)
                    logger.info("Sent: " + label + ':' + self.sent_messages[label] + ':')
                    continue
                elif label == header and received[1] == 'request':
                    data = header + ':' + message + ':'
                    to_be_sent = (self.ID + ':' + data).encode()
                    self.sent_messages[header] = data
                    self.socket.send(to_be_sent)
                    logger.info('Sent: ' + header + ':' + message)
                    return
                else:
                    raise Exception
            raise ConnectionError

        except ConnectionError:
            logger.error('Bob failed to send {0}'.format(header))
            sys.exit()
        except Exception as err:
            logger.error('Bob failed to receive {0}:\n{1}'.format(header, str(err)))
            sys.exit()