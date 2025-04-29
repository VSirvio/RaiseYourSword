import pygame

class CustomSprite(pygame.sprite.Sprite):
    def __init__(self, owner):
        super().__init__()
        self.__owner = owner

    def update(self, dt, **kwargs):
        self.__owner.update(dt, **kwargs)
