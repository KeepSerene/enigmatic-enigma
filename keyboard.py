import pygame


class Keyboard:
    def __init__(self, alphabet: str):
        self.alphabet = alphabet

    def forward_pass(self, input_letter: str):
        signal_index = self.alphabet.find(input_letter)
        return signal_index

    def backward_pass(self, input_signal_index: int):
        letter = self.alphabet[input_signal_index]
        return letter

    def draw(self, screen: pygame.Surface, x: int, y: int, bw: int, bh: int, font):
        # bw -> box width & bh -> box height
        # Draw the frame of the box
        rect = pygame.Rect(x, y, bw, bh)
        pygame.draw.rect(screen, "white", rect, width=2, border_radius=15)

        # Draw the letters
        n = len(self.alphabet)

        for i in range(n):
            letter = self.alphabet[i]
            letter = font.render(letter, True, "grey")
            letter_rect = letter.get_rect(
                center=(x + bw // 2, y + (i + 1) * bh / (n + 1))
            )
            screen.blit(letter, letter_rect)



