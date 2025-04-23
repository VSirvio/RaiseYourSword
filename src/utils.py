import os
import math

import pygame

dirname = os.path.dirname(__file__)

def fill_with_tile(canvas, tile):
    for x in range(math.ceil(canvas.get_width() / tile.get_width())):
        for y in range(math.ceil(canvas.get_height() / tile.get_height())):
            canvas.blit(tile, (x * tile.get_width(), y * tile.get_height()))

def load_animation(character, row, num_of_frames):
    sprite_sheet = pygame.image.load(
        os.path.join(dirname, "assets", f"character_{character}_animations.png")
    )

    frames = []
    for frame_num in range(num_of_frames):
        frames.append(sprite_sheet.subsurface((frame_num * 48, row * 48, 48, 48)))

    return frames
