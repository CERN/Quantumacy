import socket
import ast
import time
import select
from node import Node
from models import photon
from qexceptions import qsocketerror, qobjecterror
from threading import Thread


class sender(Node):
    def __init__(self):
        super().__init__()
        self.tokens = []

    '''
    def authenticate(self):
        try:
            print("listening to classical channel for auth token...")
            while True:
                data = self.socket.recv(self.buffer_size)
                message = data.decode()
                payload = message.split(":")
                if self.ownMessage(payload[0]):
                    continue
                if payload[2] in self.tokens:
                    self.socket.send("Success".encode())
                    #                    time.sleep(1)
                    return True
                else:
                    self.socket.send("Fail, wrong token")
                    return False
        except socket.error:
            raise qsocketerror("not connected to any channel")
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

    def create_photon_pulse(self):
        for i in range(self.photon_pulse_size):
            self.photon_pulse.append(photon())
        self.basis = [p.basis for p in self.photon_pulse]
        return self.photon_pulse

    '''
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
    '''

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

    '''
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
                raise qsocketerror("not connected to any channel")'''

    '''
    def listen_for_basis(self):
        try:
            print("listening to classical channel for basis...")
            while True:
                message = self.recv('basis')
                print("Received basis...")
                print(message)
                try:
                    literal = ast.literal_eval(message)
                except ValueError:
                    pass
                else:
                    if len(literal) > 0:
                        self.other_basis = literal
                        break
        except socket.error:
            raise qsocketerror("not connected to any channel")
    '''

    def generate_reconciled_key(self):
        if len(self.basis) != len(self.other_basis):
            raise qobjecterror("both pulses must contain the same amount of photons")

        else:
            for i in range(len(self.basis)):
                if self.basis[i] == self.other_basis[i]:
                    self.reconciled_key.append(self.basis[i])
                else:
                    self.reconciled_key.append("")

    '''    
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
    '''

    '''
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
    '''

    def send(self, header, message):
        try:
            for i in range(self.attempts):
                data = (header + ':' + message + ':')
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

    def recv(self, header):
        try:
            for i in range(self.attempts):
                data = (header + ':request:').encode()
                self.socket.send(data)
                ready = select.select([self.socket], [], [], self.timeout_in_seconds)
                if ready[0]:
                    data = self.socket.recv(self.buffer_size)
                    message = data.decode().split(':')
                    if message[1] == header:
                        print('Received: ' + header + ':' + message[2] + ':')
                        return message[2]
            raise Exception
        except ConnectionError:
            print('Alice failed to receive')


'''
    def interface_FD(self):  # trying to replicate a Full Duplex
        try:
            recvList = [self.queue._reader, self.socket]
            while True:
                data = select.select(recvList, [], [])
                for feed in data:
                    try:
                        if feed == self.socket:  # receive
                            message = self.socket.recv(self.buffer_size).decode()
                            self.entering_queue.put(message)
                    except Exception as err:
                        print("problem in interface, receiving")
                    else:
                        try:
                            self.socket.send(feed.encode())  # send
                        except Exception as err:
                            print("problem in interface, sending")
        except Exception as err:
            print("socket problem (or queue)")

    def connect_to_channel_FD(self, address, port):
        try:
            self.socket.connect((address, port))
        except socket.error:
            raise qsocketerror("unable to connect")
        try:
            self.t1 = Thread(target=self.interface_FD, args=())
            self.t1.daemon = True
            self.t1.start()

        except Exception as err:
            print("fail to create connection thread")

    def reset_socket_FD(self):
        self.socket.close()
        self.t1.join()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.t1.start()

    def authenticate_FD(self):
        try:
            print("listening to classical channel for auth token...")
            while True:
                message = self.entering_queue.get()
                payload = message.split(":")
                if self.ownMessage(payload[0]):
                    continue
                if payload[2] in self.tokens:
                    self.exiting_queue.put("Success")
                    #                    time.sleep(1)
                    return True
                else:
                    self.exiting_queue.put("Fail, wrong token")
                    return False
        except socket.error:
            raise qsocketerror("not connected to any channel")
'''
