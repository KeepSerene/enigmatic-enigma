import pygame


class Plugboard:
    def __init__(self, alphabet: str, pairs: list[str]):
        self.left = alphabet
        self.right = alphabet

        # Swap the letters in each pair in "pairs" in the left string
        for pair in pairs:
            letter1, letter2 = pair
            letter1_pos = self.left.find(letter1)
            letter2_pos = self.left.find(letter2)
            self.left = self.left[:letter1_pos] + letter2 + self.left[letter1_pos + 1 :]
            self.left = self.left[:letter2_pos] + letter1 + self.left[letter2_pos + 1 :]

    def forward_pass(self, input_signal_index: int):
        letter = self.right[input_signal_index]
        paired_letter_index = self.left.find(letter)
        return paired_letter_index

    def backward_pass(self, input_signal_index: int):
        letter = self.left[input_signal_index]
        paired_letter_index = self.right.find(letter)
        return paired_letter_index

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
            screen.blit(letter, letter_rect)

            # Draw the right string
            letter = self.right[i]
            letter = font.render(letter, True, "grey")
            letter_rect = letter.get_rect(
                center=(x + bw * (3 / 4), y + (i + 1) * bh / (n + 1))
            )
            screen.blit(letter, letter_rect)
