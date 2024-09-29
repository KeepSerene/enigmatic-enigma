from keyboard import Keyboard
from plugboard import Plugboard
from rotors import Rotor
from reflector import Reflector


class Enigma:
    def __init__(
        self,
        kb: Keyboard,
        pb: Plugboard,
        r1: Rotor,
        r2: Rotor,
        r3: Rotor,
        reflector: Reflector,
    ):
        self.kb = kb
        self.pb = pb
        self.r1 = r1  # The left most rotor
        self.r2 = r2  # The middle rotor
        self.r3 = r3  # The right most rotor
        self.reflector = reflector

    def set_rings(self, ring_setting: tuple[int, int, int]):
        self.r1.set_ring(ring_setting[0])
        self.r2.set_ring(ring_setting[1])
        self.r3.set_ring(ring_setting[2])

    def set_key(self, key: str):
        self.r1.rotate_to_letter(key[0])
        self.r2.rotate_to_letter(key[1])
        self.r3.rotate_to_letter(key[2])

    def encipher(self, letter: str) -> tuple[list[int], str]:
        # Rotate the rotors
        if self.r3.left[0] == self.r3.notch and self.r2.left[0] == self.r2.notch:
            self.r1.rotate()
            self.r2.rotate()
            self.r3.rotate()

        # The double step anomaly of the historical Enigma machine:
        elif self.r2.left[0] == self.r2.notch:
            self.r1.rotate()
            self.r2.rotate()
            self.r3.rotate()

        elif self.r3.left[0] == self.r3.notch:
            self.r2.rotate()
            self.r3.rotate()

        else:
            self.r3.rotate()

        # Pass signal through the machine
        signal_index = self.kb.forward_pass(letter)
        # To facilitate drawing the encryption path, store the same singal index twice,
        # or thrice, in case of the reflector, in each step
        encryption_path = [signal_index, signal_index]
        signal_index = self.pb.forward_pass(signal_index)
        encryption_path.append(signal_index)
        encryption_path.append(signal_index)
        signal_index = self.r3.forward_pass(signal_index)
        encryption_path.append(signal_index)
        encryption_path.append(signal_index)
        signal_index = self.r2.forward_pass(signal_index)
        encryption_path.append(signal_index)
        encryption_path.append(signal_index)
        signal_index = self.r1.forward_pass(signal_index)
        encryption_path.append(signal_index)
        encryption_path.append(signal_index)
        signal_index = self.reflector.reflect(signal_index)
        encryption_path.append(signal_index)
        encryption_path.append(signal_index)
        encryption_path.append(signal_index)
        signal_index = self.r1.backward_pass(signal_index)
        encryption_path.append(signal_index)
        encryption_path.append(signal_index)
        signal_index = self.r2.backward_pass(signal_index)
        encryption_path.append(signal_index)
        encryption_path.append(signal_index)
        signal_index = self.r3.backward_pass(signal_index)
        encryption_path.append(signal_index)
        encryption_path.append(signal_index)
        signal_index = self.pb.backward_pass(signal_index)
        encryption_path.append(signal_index)
        encryption_path.append(signal_index)
        letter = self.kb.backward_pass(signal_index)
        return (encryption_path, letter)
