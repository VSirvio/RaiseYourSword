import os

import pygame

from config import GRAPHICS_SCALING_FACTOR, DISPLAY_WIDTH, DISPLAY_HEIGHT
from utils import fill_with_tile

dirname = os.path.dirname(__file__)

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        tile = pygame.image.load(os.path.join(dirname, "..", "assets", "background_tile_grass.png"))
        tile = pygame.transform.scale_by(tile, GRAPHICS_SCALING_FACTOR)

        self.image = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        fill_with_tile(self.image, tile)

        self.rect = self.image.get_rect()
