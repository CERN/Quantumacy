import socket
import ast
from models import photon
from utils import validate
from qexceptions import qsocketerror, qobjecterror

class sender(object):
    def __init__(self):
        self.photon_pulse_size = 170
        self.min_shared = 20  # safe option
        self.photon_pulse = []
        self.buffer_size = 4096
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.basis = []
        self.other_basis = []
        self.reconciled_key = []
        self.shared_key = []
        self.sub_shared_key = []
        self.other_sub_key = []
        self.decision = 0
        self.other_decision = 0

    def create_photon_pulse(self):
        self.photon_pulse = []
        for i in range(self.photon_pulse_size):
            self.photon_pulse.append(photon())
        self.basis = [p.basis for p in self.photon_pulse]
        return self.photon_pulse

    def ownMessage(self, addr):
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        if (local_ip == addr):
            return True

        return False
        
    def generate_reconciled_key(self):
        if len(self.basis) != len(self.other_basis):
            raise qobjecterror("both pulses must contain the same amount of photons")

        else:
            for i in range(len(self.basis)):
                if self.basis[i] == self.other_basis[i]:
                    self.reconciled_key.append(self.basis[i])
                else:
                    self.reconciled_key.append("")

    def validate(self, min_shared_percent = 0.89):
        self.decision = validate(self.sub_shared_key, self.other_sub_key, min_shared_percent)
        return self.decision

    def create_keys(self):
        self.create_shared_key()
        self.create_sub_shared_key()

    def create_shared_key(self):
        for i in range(len(self.photon_pulse)):
            if self.reconciled_key[i] != "":
                self.shared_key.append(self.photon_pulse[i].bit)

    def create_sub_shared_key(self):
        self.sub_shared_key = self.shared_key[:(len(self.shared_key)//2)]

    def send_photon_pulse(self, pulse):
        if not isinstance(pulse, list):
            raise qobjecterror("argument must be list")

        try:
            message = "qpulse:"
            for p in range(len(pulse)):
                message += str(pulse[p].polarization) + "~"
            self.socket.send(message.encode())
        except socket.error:
            raise qsocketerror("not connected to any channel")

    def listen_for_basis(self):
        try:
            print("listening to classical channel for basis...")
            while True:
                data = self.socket.recv(self.buffer_size)
                message = data.decode()
                basis = message.split(":")
                if self.ownMessage(basis[0]):
                    continue
                if "basis" in message and len(basis) == 3:
                    print("Received basis...")
                    print(message)
                    try:
                        literal = ast.literal_eval(basis[2])
                    except ValueError:
                        pass
                    else:
                        if len(literal) > 0:
                            self.other_basis = literal
                            break
        except socket.error:
            raise qsocketerror("not connected to any channel")

    def listen_for_key(self):
        try:
            print("listening to classical channel for public key...")
            while True:
                data = self.socket.recv(self.buffer_size)
                message = data.decode()
                payload = message.split(":")
                if self.ownMessage(payload[0]):
                    continue
                if "key" in message and len(payload) == 3:
                    print("Received public key...")
                    print(message)
                    try:
                        literal = ast.literal_eval(payload[2])
                    except ValueError:
                        pass
                    else:
                        self.other_sub_key = literal
                        break
        except socket.error:
            raise qsocketerror("not connected to any channel")

    def listen_for_decision(self):
        try:
            print("listening to classical channel for decision...")
            while True:
                data = self.socket.recv(self.buffer_size)
                message = data.decode()
                payload = message.split(":")
                if self.ownMessage(payload[0]):
                    continue
                if "decision" in message and len(payload) == 3:
                    print("Received public key...")
                    print(message)
                    try:
                        literal = ast.literal_eval(payload[2])
                    except ValueError:
                        pass
                    else:
                        self.other_decision = literal
                        break
        except socket.error:
            raise qsocketerror("not connected to any channel")

    def send_classical_bits(self, header, bits):
        string = header + ":" + repr(bits)
        try:
            self.socket.send(string.encode())
        except socket.error:
            raise qsocketerror("not connected to any channel")

    def connect_to_channel(self, address, port):
        try:
            self.socket.connect((address, port))
        except socket.error:
            raise qsocketerror("unable to connect")

    def reset_socket(self):
        self.socket.close()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)