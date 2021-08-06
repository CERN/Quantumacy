import socket
import select
import sys
from node import Node
from models import Photon
from qexceptions import qsocketerror, qobjecterror
import re


class sender(Node):
    """Sender class, it expands Node, it contains methods to communicate a receiver node, the general idea is that this
    node dictate the communication and the receiver can just answer"""
    def __init__(self):
        super().__init__()

    def create_photon_pulse(self) -> list:
        """Create a list of photons given a size
        Returns:
             list of photons"""
        for i in range(self.photon_pulse_size):
            self.photon_pulse.append(Photon())
        self.basis = [p.basis for p in self.photon_pulse]
        return self.photon_pulse

    def send_photon_pulse(self, pulse: list):
        """Send an already created photon pulse

            it takes the polarization from each photon
            Args:
                pulse (list): photon pulse to be sent
        """
        if not isinstance(pulse, list):
            raise qobjecterror("argument must be list")
        try:
            message = ''
            for p in range(len(pulse)):
                message += str(pulse[p].polarization) + "~"
            self.send("qpulse", message)
        except socket.error:
            raise qsocketerror("not connected to any channel")

    def generate_reconciled_key(self):
        """Generate a common key between the two parties

        it checks for every photon if the chosen basis is common, if it is not common the basis is discarded
        """
        if len(self.basis) != len(self.other_basis):
            raise qobjecterror("both pulses must contain the same amount of photons")
        else:
            for i in range(len(self.basis)):
                if self.basis[i] == self.other_basis[i]:
                    self.reconciled_key.append(self.basis[i])
                else:
                    self.reconciled_key.append("")

    def send(self, header: str, message: str):
        """Sender method for sender node

        it sends a message and wait for an acknowledgment if it doesn't receive the ack in the given time
        timeout_in_seconds it may try multiple times depending on the variable connection_attempts
        Args:
            header (str): unique identifier
            message (str): string to be sent
        """
        try:

            for i in range(self.connection_attempts):
                data = (header + ':' + message + ':')
                self.socket.send(data.encode())
                print('Sent: ' + data)
                ready = select.select([self.socket], [], [], self.timeout_in_seconds)
                if ready[0]:
                    data = self.socket.recv(self.buffer_size)
                    received = data.decode().split(':')
                    if received[1] == header and received[2] == 'ack':
                        return True
            raise ConnectionError
        except ConnectionError as e:
            print('Alice failed to send:\n' + str(e))
            sys.exit()

    def recv(self, header: str):
        """Receiver method for sender node

        It will send a request message with the given header and it will wait for the response for a time
        timeout_in_seconds it may try multiple times depending on the variable connection_attempts, every received
        message with a different header will be discarded
        Args:
            header (str): unique identifier
        """
        try:
            for i in range(self.connection_attempts):
                message = ''
                data_send = (header + ':request:').encode()
                self.socket.send(data_send)
                while 1:
                    ready = select.select([self.socket], [], [], self.timeout_in_seconds)
                    if ready[0]:
                        data_recv = self.socket.recv(self.buffer_size).decode()
                        message += re.sub(self.regex, '', data_recv) #removing ('xxx.xxx.xxx.xxx', xxxx):
                        if message.count(':') >= 2:  # checking if payload started and finished
                            mess_list = message.split(':')
                            if mess_list[0] == header:
                                print('Received: ' + header + ':' + mess_list[1] + ':')
                                return mess_list[1]
                    else:
                        break
            raise Exception
        except Exception as CE:
            print('Alice failed to receive: \n' + str(CE))
            sys.exit()
