import string
import pygame
from keyboard import Keyboard
from plugboard import Plugboard
from rotors import Rotor
from reflector import Reflector
from enigma import Enigma
from draw import draw_enigma


# Set the alphabet
ALPHABET = string.ascii_uppercase

# The following wirings and turnover notch positions are taken from https://en.wikipedia.org/wiki/Enigma_rotor_details
# Historical Enigma rotors
I = Rotor(ALPHABET, "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q")
II = Rotor(ALPHABET, "AJDKSIRUXBLHWTMCQGZNPYFVOE", "E")
III = Rotor(ALPHABET, "BDFHJLCPRTXVZNYEIWGAKMUSQO", "V")
IV = Rotor(ALPHABET, "ESOVPZJAYQUIRHXLNFTGKDCMWB", "J")
V = Rotor(ALPHABET, "VZBRGITYUPSDNHLXAWMJQOFECK", "Z")

# Historical Enigma reflectors
A = Reflector(ALPHABET, "EJMZALYXVBWFCRQUONTSPIKHGD")
B = Reflector(ALPHABET, "YRUHQSLDPXNGOKMIEBFZCWVJAT")  # preferred
C = Reflector(ALPHABET, "FVPJIAOYEDRZXWGCTKUQSBNMHL")

# Keyboard and Plugboard
KB = Keyboard(ALPHABET)
PB = Plugboard(ALPHABET, ["AR", "BH", "MS"])

# Define the Enigma machine
ENIGMA = Enigma(KB, PB, IV, II, I, B)

# Ring setting: (1, 1, 1) -> "AAA", (1, 1, 2) -> "AAB", (5, 2, 3) -> "EBC", and so on
ENIGMA.set_rings((1, 1, 2))

# Set the initial letters on the three rotors, left to right
# The key is affected by ring settings
ENIGMA.set_key("CAT")

"""
# Encipher a message
msg = "A"
cipher_text = ""

for letter in msg:
    cipher_text += ENIGMA.encipher(letter.upper())

print(f"\nEncoded Message: {cipher_text}\n")
"""

# Setup Pygame
WIDTH, HEIGHT = 1300, 750
FPS = 60
MARGINS = {"top": 200, "bottom": 100, "left": 100, "right": 100}
SPACING = 70


pygame.init()

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enigma Simulator")

pygame.font.init()
REGULAR_FONT = pygame.font.SysFont("FreeMono", 25)
BOLD_FONT = pygame.font.SysFont("FreeMono", 25, bold=True)


def main():
    running = True
    clock = pygame.time.Clock()

    user_input = ""
    encryption_path = []
    encoded_output = ""

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                # if event.key == pygame.K_BACKSPACE:
                #     if user_input:
                #         user_input[:-1]
                #         encoded_output[:-1]

                elif event.key == pygame.K_DOWN:
                    II.rotate()

                elif event.key == pygame.K_SPACE:
                    user_input += " "
                    encoded_output += " "

                else:
                    key = event.unicode

                    if key in string.ascii_lowercase or key in string.ascii_uppercase:
                        letter = key.upper()
                        user_input += letter
                        encryption_path, encoded_letter = ENIGMA.encipher(letter)
                        # print(encryption_path)
                        encoded_output += encoded_letter

        SCREEN.fill("#333333")

        # Draw user input
        text = BOLD_FONT.render(user_input, 1, "white")
        text_rect = text.get_rect(center=(WIDTH / 2, MARGINS["top"] / 3))
        SCREEN.blit(text, text_rect)

        # Draw enciphered message
        text = REGULAR_FONT.render(encoded_output, 1, "white")
        text_rect = text.get_rect(center=(WIDTH / 2, MARGINS["top"] / 3 + 30))
        SCREEN.blit(text, text_rect)

        # Draw the Enigma components
        draw_enigma(
            SCREEN, ENIGMA, encryption_path, WIDTH, HEIGHT, MARGINS, SPACING, BOLD_FONT
        )

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
