import pygame
from enigma import Enigma


def draw_enigma(
    screen: pygame.Surface,
    enigma: Enigma,
    encryption_path: list[int],
    width: int,
    height: int,
    margins: dict,
    spacing: int,
    font,
):
    # Base coordinates
    x = margins["left"]
    y = margins["top"]
    box_width = (width - margins["left"] - margins["right"] - 5 * spacing) / 6
    box_height = height - y - margins["bottom"]

    # Draw the Enigma components, left to right
    for component in [
        enigma.reflector,
        enigma.r1,
        enigma.r2,
        enigma.r3,
        enigma.pb,
        enigma.kb,
    ]:
        component.draw(screen, x, y, box_width, box_height, font)
        x += box_width + spacing

    # Path coordinates
    path_y = [
        margins["top"] + (signal_index + 1) * box_height / 27
        for signal_index in encryption_path
    ]  # 27 = the length of the alphabet + 1

    # For the keyboard
    path_x = [width - margins["right"] - box_width / 2]

    # During the forward pass
    for i in [4, 3, 2, 1, 0]:
        path_x.append(margins["left"] + i * (box_width + spacing) + box_width * (3 / 4))
        path_x.append(margins["left"] + i * (box_width + spacing) + box_width * (1 / 4))

    # For the reflector
    path_x.append(margins["left"] + box_width * (3 / 4))

    # During the backward pass
    for i in [1, 2, 3, 4]:
        path_x.append(margins["left"] + i * (box_width + spacing) + box_width * (1 / 4))
        path_x.append(margins["left"] + i * (box_width + spacing) + box_width * (3 / 4))

    # For the lampboard
    path_x.append(width - margins["right"] - box_width / 2)

    # Draw the encryption path
    if encryption_path:
        for i in range(1, len(encryption_path)):
            if i < 10:
                color = "#43aa8b"
            elif 10 <= i < 12:
                color = "#f9c74f"
            else:
                color = "#e63946"

            start = (path_x[i - 1], path_y[i - 1])
            end = (path_x[i], path_y[i])
            pygame.draw.line(screen, color, start, end, width=4)

    # Draw labels of the components
    labels = ["Reflector", "Left", "Middle", "Right", "Plugboard", "Keys/Lamps"]
    label_x = margins["left"] + box_width / 2
    label_y = margins["top"] * 0.85

    for i in range(len(labels)):
        label = font.render(labels[i], 1, "white")
        label_rect = label.get_rect(center=(label_x, label_y))
        screen.blit(label, label_rect)
        label_x += box_width + spacing
