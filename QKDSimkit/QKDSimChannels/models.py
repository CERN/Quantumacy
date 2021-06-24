import random

class photon(object):
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

    def measure(self, eigenstate):
        if (eigenstate == "RL"):
            return random.choice([0, 90])
        elif (eigenstate == "DG"):
            return random.choice([45, 135])
        else:
            return self.polarization
