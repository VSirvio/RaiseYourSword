import os
import math

import pygame

from config import GRAPHICS_SCALING_FACTOR

dirname = os.path.dirname(__file__)

def fill_with_tile(canvas, tile):
    for x in range(math.ceil(canvas.get_width() / tile.get_width())):
        for y in range(math.ceil(canvas.get_height() / tile.get_height())):
            canvas.blit(tile, (x * tile.get_width(), y * tile.get_height()))

def load_animation(character, row, num_of_frames):
    sprite_sheet = pygame.image.load(os.path.join(dirname, "assets", f"character_{character}_animations.png"))
    sprite_sheet = pygame.transform.scale_by(sprite_sheet, GRAPHICS_SCALING_FACTOR)

    frames = []
    for frame_num in range(num_of_frames):
        frames.append(sprite_sheet.subsurface((
            frame_num * GRAPHICS_SCALING_FACTOR * 48,
            row * GRAPHICS_SCALING_FACTOR * 48,
            GRAPHICS_SCALING_FACTOR * 48,
            GRAPHICS_SCALING_FACTOR * 48
        )))

    return frames
