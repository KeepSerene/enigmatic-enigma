import pygame


class Reflector:
    def __init__(self, alphabet: str, wiring: str):
        self.left = alphabet
        self.right = wiring

    def reflect(self, input_signal_index: int):
        letter = self.right[input_signal_index]
        paired_letter_index = self.left.find(letter)
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
                center=(x + bw // 4, y + (i + 1) * bh / (n + 1))
            )
            screen.blit(letter, letter_rect)

            # Draw the right string
            letter = self.right[i]
            letter = font.render(letter, True, "grey")
            letter_rect = letter.get_rect(
                center=(x + bw * (3 / 4), y + (i + 1) * bh / (n + 1))
            )
            screen.blit(letter, letter_rect)
