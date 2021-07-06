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

    def importkey(self):
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

    '''
    def listen_for_key(self, key_owner: str):
        try:
            print("listening to classical channel for public key...")
            while True:
                message = self.recv(key_owner + '-key')
                print("Received public key...")
                print(message)
                try:
                    literal = ast.literal_eval(message)
                except ValueError:
                    pass
                else:
                    self.other_sub_key = literal
                    break
        except socket.error:
            raise qsocketerror("not connected to any channel")
    '''

    '''
    def listen_for_decision(self, decider: str):
        try:
            print("listening to classical channel for decision...")
            while True:
                message = self.recv(decider + '-decision')
                print("Received decision...")
                print(message)
                try:
                    literal = ast.literal_eval(message)
                except ValueError:
                    pass
                else:
                    self.other_decision = literal
                    break
        except socket.error:
            raise qsocketerror("not connected to any channel")
    '''

    def validate(self, min_shared_percent=0.89):
        self.decision = validate(self.sub_shared_key, self.other_sub_key, min_shared_percent)
        return self.decision

    def send(self):
        print("send(): Override me")

    def receive(self):
        print("receive(): Override me")

    '''
    def recv_safe(self, expected: str) -> str:
        try:
            while True:
                data = self.socket.recv(self.buffer_size)
                message = data.decode().split(":")
                label = message[1]
                ack = label+":ack"
                if label != expected and label in self.sent_acks:
                    self.socket.send(ack.encode())
                    continue
                elif label != expected and label not in self.sent_acks:
                    raise Exception
                self.socket.send(ack.encode())
                self.sent_acks.append(label)
                return message[2]
        except Exception:
            print("failed to receive safely")
    '''

    '''
    def send_safe(self, header: str, message: str) -> bool:
        try:
            for i in range(self.attempts):
                data = (header + ':' + message).encode()
                self.socket.send(data)
                ready = select.select([self.socket], [], [], self.timeout_in_seconds)
                if ready[0]:
                    data = self.socket.recv(self.buffer_size)
                    message = data.decode().split(':')
                    if message[1] == header:
                        if message[2] == 'ack':
                            return True
        except Exception:
            print()
    '''