import pygame


class Rotor:
    def __init__(self, alphabet: str, wiring: str, notch: str):
        self.alphabet = alphabet
        self.left = self.alphabet
        self.right = wiring
        self.notch = notch

    def forward_pass(self, input_signal_index: int):
        letter = self.right[input_signal_index]
        paired_letter_index = self.left.find(letter)
        return paired_letter_index

    def backward_pass(self, input_signal_index: int):
        letter = self.left[input_signal_index]
        paired_letter_index = self.right.find(letter)
        return paired_letter_index

    def rotate(self, step=1, is_forward=True):
        for _ in range(step):
            if is_forward:
                self.left = self.left[1:] + self.left[0]
                self.right = self.right[1:] + self.right[0]
            else:
                self.left = self.left[-1] + self.left[:-1]
                self.right = self.right[-1] + self.right[:-1]

    def rotate_to_letter(self, letter: str):
        step = self.alphabet.find(letter)
        self.rotate(step)

    def set_ring(self, ring_setting: int):
        # Rotate the rotor backward | "ring_setting" starts from 1, so subtract 1 from it for indexing
        self.rotate(ring_setting - 1, is_forward=False)

        # Adjust the turnover notch in relation to the wiring
        notch_index = self.alphabet.find(self.notch)
        self.notch = self.alphabet[
            (notch_index - ring_setting + 1) % len(self.alphabet)
        ]

    def display(self):
        print(self.left)
        print(self.right)
        print()

    def draw(self, screen: pygame.Surface, x: int, y: int, bw: int, bh: int, font):
        # bw -> box width & bh -> box height
        # Draw the frame of the box
        rect = pygame.Rect(x, y, bw, bh)
        pygame.draw.rect(screen, "white", rect, width=2, border_radius=15)

        # Draw the letters
        n = len(self.left)

        for i in range(n):
            # Draw the left string
            letter = self.left[i]
            letter = font.render(letter, True, "grey")
            letter_rect = letter.get_rect(
                center=(x + bw * (1 / 4), y + (i + 1) * bh / (n + 1))
            )

            # Highlight the top letter in the left string
            if i == 0:
                pygame.draw.rect(screen, "teal", letter_rect, border_radius=5)

            # Highlight the notch in the left string
            if self.left[i] == self.notch:
                letter = font.render(self.notch, True, "#333333")
                pygame.draw.rect(screen, "white", letter_rect, border_radius=5)

            screen.blit(letter, letter_rect)

            # Draw the right string
            letter = self.right[i]
            letter = font.render(letter, True, "grey")
            letter_rect = letter.get_rect(
                center=(x + bw * (3 / 4), y + (i + 1) * bh / (n + 1))
            )
            screen.blit(letter, letter_rect)
