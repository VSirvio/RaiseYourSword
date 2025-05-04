import os
import math

import pygame

dirname = os.path.dirname(__file__)

def fill_with_tile(canvas, tile):
    """Fills a pygame surface by repeating a smaller pygame surface.

    Args:
        canvas: A pygame surface to fill.
        tile: A smaller pygame surface that the other surface is filled with.
    """

    for x in range(math.ceil(canvas.get_width() / tile.get_width())):
        for y in range(math.ceil(canvas.get_height() / tile.get_height())):
            canvas.blit(tile, (x * tile.get_width(), y * tile.get_height()))

def load_animation(character, row, num_of_frames, column=0):
    """Loads animation frames from a sprite sheet in the "assets" directory.

    Args:
        character: Character name as a string (e.g. "warrior", "skeleton").
        row: Number of the row where the animation is in the sprite sheet.
        num_of_frames: Total number of frames in the animation.
        column: Number of the column where the animation is in the sprite sheet.

    Returns:
        A list of pygame surfaces. The length of the list is <num_of_frames>.
    """

    global sprite_sheets

    try:
        sprite_sheets
    except NameError:
        sprite_sheets = {}

    if character not in sprite_sheets:
        sprite_sheets[character] = pygame.image.load(
            os.path.join(dirname, "assets", f"character_{character}_animations.png")
        )

    frames = []
    for frame_num in range(num_of_frames):
        frames.append(sprite_sheets[character].subsurface(((column + frame_num) * 48, row * 48, 48, 48)))

    return frames
