import os
import math

import pygame

dirname = os.path.dirname(__file__)

def centered(rect, canvas_size):
    canvas_width, canvas_height = canvas_size

    x_coordinate = (canvas_width - rect.width) // 2
    y_coordinate = (canvas_height - rect.height) // 2

    return pygame.Rect(x_coordinate, y_coordinate, rect.width, rect.height)

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
