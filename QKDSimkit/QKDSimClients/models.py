import random


class Photon(object):
    def __init__(self):
        self.bit = self.create_random_bit()
        self.basis = self.select_random_basis()
        self.polarization = self.set_polarization()

    def create_random_bit(self):
        return random.randint(0, 1)

    def select_random_basis(self):
        return random.choice(["RL", "DG"])  # RL = Rectilinear basis; DG = Diagonal basis;

    def set_polarization(self):  # Set polarization according to settings of bits and basis.
        if (self.basis == "RL" and self.bit == 0):
            return 0
        elif (self.basis == "RL" and self.bit == 1):
            return 90
        elif (self.basis == "DG" and self.bit == 0):
            return 45
        elif (self.basis == "DG" and self.bit == 1):
            return 135

        return self.polarization

    def measure(self, polarization):
        if (self.basis == "RL"):
            if polarization in [0, 90]:
                return polarization
            else: 
                return random.choice([0, 90])
        elif (self.basis == "DG"):
            if polarization in [45, 135]:
                return polarization
            else: 
                return random.choice([45, 135])

    def set_bit_from_measurement(self):  # Set bits according to settings of polarization and basis.
        if (self.basis == "RL" and self.polarization == 0):
            return 0
        elif (self.basis == "RL" and self.polarization == 90):
            return 1
        elif (self.basis == "DG" and self.polarization == 45):
            return 0
        elif (self.basis == "DG" and self.polarization == 135):
            return 1

        return self.bit

