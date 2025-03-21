import pygame

from sprites.background import Background

class Game:
    def __init__(self):
        self.__background = Background()
        self.__all_sprites = pygame.sprite.Group(self.__background)

    def draw(self, surface):
        self.__all_sprites.draw(surface)
