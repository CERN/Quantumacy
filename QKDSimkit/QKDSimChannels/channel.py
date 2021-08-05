import socket
import sys
from threading import Thread
from qexceptions import qsocketerror
from channel_features import eavesdropper
from channel_features import random_errors

import json


class public_channel(object):  # insecure public classical/quantum channel
    def __init__(self):
        self.__dict__ = json.load(open('../config.json',))['channel']
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # reusable socket
        self.ip_list = []  # blacklist already created connections
        self.conn_list = []
        self.full_data = []

    def initiate_channel(self, *port):
        """Start channel"""
        if len(port) > 0:
            self.port = str(port[0])

        try:
            self.socket.bind((self.host, self.port))
        except socket.error:
            raise qsocketerror("port {0} is occupied".format(self.port))

        self.socket.listen(1)

        print("initiated the channel on {0}:{1}, waiting for clients...".format(self.host, self.port))

        while True:
            conn, addr = self.socket.accept()  # initiate new serving thread for every new connection:
            if conn not in self.conn_list:
                print("{0} has connected.".format(addr))
                self.ip_list.append(addr)
                self.conn_list.append(conn)
                _thread = Thread(target=self.initiate_connection, args=(conn, addr))
                _thread.daemon = True
                _thread.start()
            else:
                print(self.ip_list)

    def initiate_connection(self, conn, addr):
        """Listen for messages and broadcast them"""
        while True:
            try:
                data = conn.recv(self.buffer_size)
                message = data.decode()
                if message.split(':')[0] == 'qpulse' and message.split(':')[1] != 'ack':
                    if self.eve:
                        message = eavesdropper(str(message).split(':', 1)[1])
                    if self.noise > 0:
                        message = random_errors(str(message).split(':', 1)[1], self.noise)
            except ConnectionResetError:
                break
            except ConnectionAbortedError:
                break


            if not message:
                break
            else:
                fwdMessage = "{0}:{1}".format(addr, message)
                print(fwdMessage)
                for clients in self.conn_list:
                    try:
                        if clients.getpeername() != addr:
                            clients.sendall(fwdMessage.encode())
                    except OSError:
                        # old connections?
                        print("Ünknown connection, ignoring...")

        conn.close()
        self.conn_list.remove(conn)
        self.ip_list.remove(addr)

        print(str(addr) + " has disconnected")
