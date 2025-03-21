import os

import pygame

from config import GRAPHICS_SCALING_FACTOR

FRAMETIME = 250
SPRITE_WIDTH = 48
SPRITE_HEIGHT = 48

dirname = os.path.dirname(__file__)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        sprite_sheet = pygame.image.load(os.path.join(dirname, "..", "assets", "char_warrior_idle_down.png"))
        sprite_sheet = pygame.transform.scale_by(sprite_sheet, GRAPHICS_SCALING_FACTOR)

        self.images = []
        for i in range(5):
            self.images.append(
                pygame.Surface((GRAPHICS_SCALING_FACTOR * SPRITE_WIDTH, GRAPHICS_SCALING_FACTOR * SPRITE_HEIGHT), pygame.SRCALPHA)
            )
            self.images[-1].blit(sprite_sheet, (-i * GRAPHICS_SCALING_FACTOR * SPRITE_WIDTH, 0))

        self.index = 0

        self.image = self.images[self.index]

        self.rect = self.image.get_rect()

        self.timer = 0

    def update(self, dt):
        self.timer += dt

        while self.timer >= FRAMETIME:
            self.index = (self.index + 1) % 5
            self.timer -= FRAMETIME

        self.image = self.images[self.index]
