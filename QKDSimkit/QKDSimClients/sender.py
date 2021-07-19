import socket
import ast
import time
import select
import sys
from node import Node
from models import photon
from qexceptions import qsocketerror, qobjecterror
from threading import Thread


class sender(Node):
    def __init__(self):
        super().__init__()
        self.tokens = []
    '''
    def authenticate(self) -> bool:
        try:
            print("listening to classical channel for auth token...")
            while True:
                message = self.recv("token")
                if message in self.tokens:
                    print("Successful authentication")
                    self.send("result", "Success")
                    return True
                else:
                    self.send("result", "Fail, wrong token")
                    return False
        except ConnectionError:
            raise qsocketerror("Authentication error")
            sys.exit()
    '''
    def create_photon_pulse(self):
        for i in range(self.photon_pulse_size):
            self.photon_pulse.append(photon())
        self.basis = [p.basis for p in self.photon_pulse]
        return self.photon_pulse

    def send_photon_pulse(self, pulse):
        if not isinstance(pulse, list):
            raise qobjecterror("argument must be list")
        try:
            message = ''
            for p in range(len(pulse)):
                message += str(pulse[p].polarization) + "~"

            self.send("qpulse", message)
        except socket.error:
            raise qsocketerror("not connected to any channel")
            sys.exit()

    def generate_reconciled_key(self):
        if len(self.basis) != len(self.other_basis):
            raise qobjecterror("both pulses must contain the same amount of photons")

        else:
            for i in range(len(self.basis)):
                if self.basis[i] == self.other_basis[i]:
                    self.reconciled_key.append(self.basis[i])
                else:
                    self.reconciled_key.append("")

    def send(self, header, message):
        try:
            for i in range(self.attempts):
                data = (header + ':' + message + ':')
                print(str(len(data)))
                self.socket.send(data.encode())
                print('Sent: ' + data)
                ready = select.select([self.socket], [], [], self.timeout_in_seconds)
                if ready[0]:
                    data = self.socket.recv(self.buffer_size)
                    received = data.decode().split(':')
                    if received[1] == header and received[2] == 'ack':
                        return True
        except ConnectionError:
            print('Alice failed to send')
            sys.exit()

    def recv(self, header):
        try:
            for i in range(self.attempts):
                data = (header + ':request:').encode()
                self.socket.send(data)
                ready = select.select([self.socket], [], [], self.timeout_in_seconds)
                if ready[0]:
                    data = self.socket.recv(self.buffer_size)
                    print(len(data))
                    message = data.decode().split(':')
                    if message[1] == header:
                        print('Received: ' + header + ':' + message[2] + ':')
                        return message[2]
            raise ConnectionError
        except ConnectionError:
            print('Alice failed to receive')
            sys.exit()
