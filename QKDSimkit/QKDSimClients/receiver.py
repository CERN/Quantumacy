import socket
import ast
from models import photon
from utils import validate
from qexceptions import qsocketerror, qobjecterror

# TODO: make multithreaded classical receiver & sender

class receiver(object):
    def __init__(self):
        self.min_shared = 20  # safe option
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buffer_size = 4096
        self.photon_pulse = []
        self.basis = []
        self.polarization_vector = []
        self.other_basis = []
        self.reconciled_key = []
        self.shared_key = []
        self.sub_shared_key = []
        self.other_sub_key = []
        self.decision = 0
        self.other_decision = 0

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
                data = self.socket.recv(self.buffer_size)
                message = data.decode()
                pulse = message.split(":")
                if "qpulse" in message and len(pulse) == 3:
                    print("Received photon pulse...")
                    print(message)
                    self.polarization_vector = pulse[2].split("~")[:-1]
                    break
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
                            self.reconciled_key = literal
                            break
        except socket.error:
            raise qsocketerror("not connected to any channel")

    def listen_for_rec_key(self):
        try:
            print("listening to classical channel for public key...")
            while True:
                data = self.socket.recv(self.buffer_size)
                message = data.decode()
                payload = message.split(":")
                if self.ownMessage(payload[0]):
                    continue
                if "rec_key" in message and len(payload) == 3:
                    print("Received public key...")
                    print(message)
                    try:
                        literal = ast.literal_eval(payload[2])
                    except ValueError:
                        pass
                    else:
                        self.reconciled_key = literal
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

    def create_photon_pulse(self, pulse_size):
        photon_pulse = []
        for i in range(1, pulse_size):
            photon_pulse.append(photon())
        return photon_pulse

    def ownMessage(self, addr):
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        if (local_ip == addr):
            return True

        return False
        
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

    def verify(self):
        if len(self.shared_key) == 0 or len(self.sub_shared_key) == 0:
            raise qobjecterror("key is not defined")
        else:
            pass

    def connect_to_channel(self, address, port):
        try:
            self.socket.connect((address, port))
        except socket.error:
            raise qsocketerror("unable to connect")

    def reset_socket(self):
        self.socket.close()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
