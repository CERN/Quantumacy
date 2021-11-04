import random
import sys
import logging
from QKDSimkit.QKDSimChannels.models import Photon


def eavesdropper(photon_stream: str) -> str:
    """Method to simulate an eavesdropper in a quantum channel
    Args:
        photon_stream (str): message containing polarizations
    Returns:
        message with new (eavesdropped) polarizations
    """
    try:
        photon_pulse = []
        new_message = 'qpulse:'
        polarization_vector = photon_stream.split("~")[:-1]
        for p in range(len(polarization_vector)):
            photon_pulse.append(Photon())
            photon_pulse[p].polarization = photon_pulse[p].measure(int(polarization_vector[p]))
            photon_pulse[p].bit = photon_pulse[p].set_bit_from_measurement()
            new_message += str(photon_pulse[p].polarization) + '~'
        return new_message
    except Exception as e:
        logging.error('Eavesdropper error:\n' + str(e))
        sys.exit()

def random_errors(photon_stream: str, rate: float) -> str:
    """Method to simulate random errors in a quantum channel
    Args:
        photon_stream (str): message containing polarizations
        rate (float): decimal number from 0 to 1, it sets the error rate
    Returns:
        message with errors
    """
    try:
        polarization_vector = photon_stream.split("~")[:-1]
        new_message = 'qpulse:'
        count = 0
        for p in polarization_vector:
            if random.randint(1, 100) <= rate*100:
                polarization = random.randint(0, 3) * 45
                new_message += str(polarization) + '~'
                count += 1
            else:
                new_message += str(p) + '~'
        logging.info('Errors: ' + str(count))
        return new_message
    except Exception as e:
        logging.error("Failed to add errors in photon stream:\n" + str(e))
        sys.exit()
