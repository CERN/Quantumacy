import socket
import ast
import logging
import json
import select
import re
import abc
from cryptography.fernet import Fernet
from QKDSimkit.QKDSimClients.utils import validate
from QKDSimkit.QKDSimChannels.qexceptions import qsocketerror


class Node(object):
    """Father class for receiver and sender
    """

    def __init__(self, ID, size):
        self.__dict__ = json.load(open('../config.json', ))['node']
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ID = ID
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
        self.photon_pulse_size = size * 5
        # self.token = self.get_key_from_password(password)

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
            logging.info("Failed to reset socket:\n" + str(e))
            raise ConnectionError

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
            logging.info("Listening to classical channel for " + attr)
            while True:
                message = self.recv(sender + '-' + attr)
                try:
                    literal = ast.literal_eval(message)
                except ValueError as VE:
                    logging.error("Value Error: " + str(VE))
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
        logging.info('Correct bits percentage: ' + str(percent))
        if percent == 1:
            return 1
        if self.min_shared_percent <= percent < 1:
            return 0
        if percent < self.min_shared_percent:
            return -1

    # def encrypt_not_qpulse(self, header: str, message: str):
    #     """encrypt payload
    #     encrypt the payload of a message if the header is not 'qpulse'
    #
    #     Returns:
    #         encrypted message (str): string made by header and encrypted payload to split parts there are ':'
    #     """
    #     if header != 'qpulse':
    #         cipher = Fernet(self.token)
    #         enc_message = cipher.encrypt(message.encode())
    #         return header + ':' + enc_message.decode() + ':'
    #     else:
    #         return header + ':' + message + ':'

    # def decrypt_not_qpulse(self, header: str, message: str):
    #     """ decrypt payload
    #     decrypt the payload of a message if the header is not 'qpulse'
    #
    #     Returns:
    #         decrypted message (str): string with decrypted payload, note that the header is not included
    #     """
    #     if header != 'qpulse':
    #         cipher = Fernet(self.token)
    #         message = cipher.decrypt(bytes(message.encode()))
    #         return message.decode()
    #     else:
    #         return message

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
    def send(self):
        """abstract method"""
        print("send(): Override me")

    @abc.abstractmethod
    def recv(self):
        """abstract method"""
        print("receive(): Override me")


    # def get_key_from_password(self, password: str) -> bytes:
    #     """ it uses a password to generate a base64, urlsafe, encrypted key
    #     Args:
    #         password (str): password to use to generate the key
    #     Returns:
    #         key (bytearray): key encrypted with the password
    #     """
    #     salt = os.urandom(16)
    #     kdf = PBKDF2HMAC(
    #         algorithm=hashes.SHA256(),
    #         length=32,
    #         salt=salt,
    #         iterations=100000,
    #         backend=default_backend()
    #     )
    #     key = base64.urlsafe_b64encode(kdf.derive(bytes(password, 'utf-8')))
    #     return key
    #
