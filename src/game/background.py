import os

import pygame

from .graphics_utils import fill_with_tile

dirname = os.path.dirname(__file__)

class Background(pygame.sprite.Sprite):
    """A sub class of pygame Sprite for the game background image."""

    def __init__(self, width, height):
        """Creates a background sprite with the given width and height.

        Args:
            width: An integer indicating width of the background in pixels.
            height: An integer indicating height of the background in pixels.
        """

        super().__init__()

        tile = pygame.image.load(
            os.path.join(dirname, "..", "assets", "background_tile_grass.png")
        )

        self.image = pygame.Surface((width, height))
        fill_with_tile(self.image, tile)

        self.rect = self.image.get_rect()
