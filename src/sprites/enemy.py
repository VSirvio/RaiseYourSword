import pygame

from config import GRAPHICS_SCALING_FACTOR

BOUNDING_BOX = pygame.Rect((20, 22), (8, 11))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, animations):
        super().__init__()

        self.__direction = "down"
        self.__state = "idle"

        self.__animations = animations

        self.__index = 0

        self.image = self.__animations[self.__state][self.__direction][self.__index]

        self.rect = self.image.get_rect()
        self.rect.x = 600
        self.rect.y = 81

        self.__timer = 0

    def update(self, dt, enemy):
        self.__timer += dt

        frametime = 1000 / self.__animations[self.__state]["framerate"]
        while self.__timer >= frametime:
            num_of_frames = len(self.__animations[self.__state][self.__direction])
            self.__index = (self.__index + 1) % num_of_frames
            self.__timer -= frametime

        self.image = self.__animations[self.__state][self.__direction][self.__index]

    @property
    def bounding_box(self):
        return pygame.Rect(
            self.rect.x + GRAPHICS_SCALING_FACTOR * BOUNDING_BOX.x,
            self.rect.y + GRAPHICS_SCALING_FACTOR * BOUNDING_BOX.y,
            GRAPHICS_SCALING_FACTOR * BOUNDING_BOX.width,
            GRAPHICS_SCALING_FACTOR * BOUNDING_BOX.height
        )
