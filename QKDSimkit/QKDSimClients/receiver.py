import socket
import ast
import sys
from node import Node
from models import photon
from qexceptions import qsocketerror, qobjecterror


# TODO: make multithreaded classical receiver & sender

class receiver(Node):
    def __init__(self):
        super().__init__()
        self.polarization_vector = []
        self.token = ''
        self.sent_acks = []
        self.sent_messages = {}
    '''
    def authenticate(self) -> bool:
        try:
            print("Sending authentication token")
            self.send("token", self.token)
            result = self.recv("result")
            print(result)
            if result == "Success":
                return True
            else:
                return False
        except ConnectionError:
            raise qsocketerror("Authentication error")
            sys.exit()
    '''
    def measure_photon_pulse(self):
        for p in range(len(self.polarization_vector)):
            self.photon_pulse.append(photon())
            self.photon_pulse[p].polarization = self.photon_pulse[p].measure(int(self.polarization_vector[p]))
            self.photon_pulse[p].bit = self.photon_pulse[p].set_bit_from_measurement()
        self.basis = [p.basis for p in self.photon_pulse]

    def listen_quantum(self):
        try:
            print("listening to quantum channel for photon pulse...")
            while True:
                message = self.recv('qpulse')
                print("Received photon pulse...")
                print(message)
                self.polarization_vector = message.split("~")[:-1]
                break
        except socket.error:
            raise qsocketerror("not connected to any channel")
            sys.exit()

    def recv(self, header: str) -> str:
        try:
            while True:
                data = self.socket.recv(self.buffer_size)
                message = data.decode().split(':')
                label = message[1]
                if label != header and label in self.sent_acks:
                    self.socket.send((label + ":ack:").encode())
                    continue
                elif label != header and label in self.sent_messages:
                    self.socket.send((label + ":" + self.sent_messages[label] + ':').encode())
                    continue
                self.socket.send((header + ":ack:").encode())
                self.sent_acks.append(label)
                print("Received: " + header + ":" + message[2])
                return message[2]
        except ConnectionError:
            print("Bob failed to receive")
            sys.exit()

    def send(self, header: str, message: str):
        try:
            while True:
                data = self.socket.recv(self.buffer_size)
                request = data.decode().split(':')
                label = request[1]
                if label != header and label in self.sent_acks:
                    self.socket.send((label + ':ack:').encode())
                    print("Sent: " + header + ':ack:')
                    continue
                elif label != header and label in self.sent_messages:
                    self.socket.send((label + ':' + self.sent_messages[label] + ':').encode())
                    print("Sent: " + header + ':' + self.sent_messages[label] + ':')
                    continue
                self.socket.send((header + ':' + message + ':').encode())
                print("Sent: " + header + ':' + message)
                self.sent_messages[header] = message
                return True
        except ConnectionError:
            print("Bob failed to send")
            sys.exit()
