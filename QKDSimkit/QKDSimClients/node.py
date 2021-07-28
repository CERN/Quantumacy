import socket
import ast
import time
import select
import json
from qexceptions import qsocketerror, qobjecterror
from utils import validate

class Node(object):
    def __init__(self):
        self.__dict__ = json.load(open('../config.json',))['node']
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.photon_pulse = []
        self.basis = []
        self.other_basis = []
        self.reconciled_key = []
        self.shared_key = []
        self.sub_shared_key = []
        self.other_sub_key = []
        self.decision = 0
        self.other_decision = 0
        self.not_shared_key = []
        self.key = []
        self.fragments = []

    def connect_to_channel(self, address, port):
        try:
            self.socket.connect((address, port))
        except socket.error:
            raise qsocketerror("unable to connect")

    def reset_socket(self):
        self.socket.close()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def ownMessage(self, addr):
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        if (local_ip == addr):
            return True
        return False

    def send_classical_bits(self, header, bits):
        string = header + ":" + repr(bits)
        try:
            self.socket.send(string.encode())
        except socket.error:
            raise qsocketerror("not connected to any channel")

    def create_keys(self):
        self.create_shared_key()
        self.create_sub_shared_key()

    def create_shared_key(self):
        for i in range(len(self.photon_pulse)):
            if self.reconciled_key[i] != "":
                self.shared_key.append(self.photon_pulse[i].bit)

    def create_sub_shared_key(self):
        self.sub_shared_key = self.shared_key[:(len(self.shared_key)//2)]

    def get_key(self):
        self.key = self.shared_key[(len(self.shared_key)//2):]

    def listen_for(self, sender: str, attr: str):
        try:
            print("Listening to classical channel for " + attr)
            while True:
                message = self.recv(sender + '-' + attr)
                try:
                    literal = ast.literal_eval(message)
                except ValueError:
                    pass
                else:
                    setattr(self, attr, literal)
                    break
        except socket.error:
            raise qsocketerror("not connected to any channel")

    def validate(self):
        percent = validate(self.sub_shared_key, self.other_sub_key)
        print('Correct bits percentage: ' + str(percent))
        if percent == 1:
            return 1
        if self.min_shared_percent <= percent < 1:
            return 0
        if percent < self.min_shared_percent:
            return -1

    def send(self):
        print("send(): Override me")

    def recv(self):
        print("receive(): Override me")