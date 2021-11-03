import socket
import sys
import logging
from QKDSimkit.QKDSimClients.node import Node
from QKDSimkit.QKDSimChannels.models import Photon
from QKDSimkit.QKDSimChannels.qexceptions import qsocketerror, qobjecterror

logging.basicConfig(level=logging.DEBUG)


class sender(Node):
    """Sender class, it expands Node, it contains methods to communicate a receiver node, the general idea is that this
    node dictate the communication and the receiver can just answer"""

    def __init__(self, ID, size: int):
        super().__init__(ID, size)

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
            #data = self.encrypt_not_qpulse(header, message)
            data = header + ':' + message + ':'
            to_be_sent = (self.ID + ':' + data).encode()
            for i in range(self.connection_attempts):
                self.socket.send(to_be_sent)
                logging.info('Sent: ' + header + ':' + message)
                received = self.recv_all()
                if not received:
                    continue
                if received[0] == header and received[1] == 'ack':
                    return
            raise ConnectionError
        except Exception as err:
            logging.error('Alice failed to send {0}:\n{1}'.format(header, str(err)))
            sys.exit()
        except ConnectionError as e:
            logging.error('Alice tried to receive too many times \n' + str(e))
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
                to_be_sent = (self.ID + ':' + header + ':request:').encode()
                self.socket.send(to_be_sent)
                received = self.recv_all()
                if not received:
                    continue
                if received[0] == header:
                    # dec_message = self.decrypt_not_qpulse(received[0], received[1])
                    dec_message = received[1]
                    logging.info("Received: " + header + ":" + dec_message)
                    return dec_message
            raise ConnectionError
        except Exception as CE:
            logging.error('Alice failed to receive: \n' + str(CE))
            sys.exit()
        except ConnectionError:
            logging.error("Alice tried to receive too many times ")
