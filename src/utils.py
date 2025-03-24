import os
import math

import pygame

from config import GRAPHICS_SCALING_FACTOR

dirname = os.path.dirname(__file__)

def centered(rect, canvas_size):
    canvas_width, canvas_height = canvas_size

    x_coordinate = (canvas_width - rect.width) / 2
    x_coordinate = round_to_precision(x_coordinate, precision=GRAPHICS_SCALING_FACTOR)

    y_coordinate = (canvas_height - rect.height) / 2
    y_coordinate = round_to_precision(y_coordinate, precision=GRAPHICS_SCALING_FACTOR)

    return pygame.Rect(x_coordinate, y_coordinate, rect.width, rect.height)

def fill_with_tile(canvas, tile):
    for x in range(math.ceil(canvas.get_width() / tile.get_width())):
        for y in range(math.ceil(canvas.get_height() / tile.get_height())):
            canvas.blit(tile, (x * tile.get_width(), y * tile.get_height()))

def floor_with_precision(number, precision):
    return number - number % precision

def load_animation(character, row, num_of_frames):
    sprite_sheet = pygame.image.load(
        os.path.join(dirname, "assets", f"character_{character}_animations.png")
    )
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

def round_to_precision(number, precision):
    return floor_with_precision(number + precision / 2, precision)
