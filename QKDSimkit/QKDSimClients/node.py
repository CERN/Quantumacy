import socket
import ast
import re
import json
from qexceptions import qsocketerror, qobjecterror
from utils import validate

class Node(object):
    """Father class for receiver and sender
    """
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
        self.regex = r'\((.)*\):'


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
            print("Failed to reset socket:\n" + str(e))
            raise ConnectionError

    def ownMessage(self, addr: str) -> bool:
        """Check if a message comes from this node

        Args:
            addr (str): address of the received message
        """
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        if (local_ip == addr):
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
        self.sub_shared_key = self.shared_key[:(len(self.shared_key)//2)]

    def get_key(self):
        """Create the part of the key that will not be sent and it will be used as symmetric key (second half)"""
        self.key = self.shared_key[(len(self.shared_key)//2):]

    def listen_for(self, sender: str, attr: str):
        """Receive a message and store it in the right place
        Args:
            sender (str): name of the node from which we expect to receive
            attr (str): name of the attribute that will store the content of the received message
            """
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

    def validate(self) -> int:
        """Wrapper of utils.validate it manages different outputs, it also gives info of eventual errors
            Returns:
                1: keys are equals
                0: error rate is below a given percent
                -1: error rate too high"""
        percent = validate(self.sub_shared_key, self.other_sub_key)
        print('Correct bits percentage: ' + str(percent))
        if percent == 1:
            return 1
        if self.min_shared_percent <= percent < 1:
            return 0
        if percent < self.min_shared_percent:
            return -1

    def send(self):
        """abstract method"""
        print("send(): Override me")

    def recv(self):
        """abstract method"""
        print("receive(): Override me")