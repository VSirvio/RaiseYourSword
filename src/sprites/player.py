import pygame

from utils import load_animation

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.__direction = "down"
        self.__state = "idle"

        self.__animations = {
            "idle": {
                "framerate": 4,
                "down": load_animation("warrior", 0, 5),
                "up": load_animation("warrior", 1, 5),
                "left": load_animation("warrior", 2, 5),
                "right": load_animation("warrior", 3, 5)
            },
            "walk": {
                "framerate": 4,
                "down": load_animation("warrior", 4, 8),
                "up": load_animation("warrior", 5, 8),
                "left": load_animation("warrior", 6, 8),
                "right": load_animation("warrior", 7, 8)
            },
            "attack": {
                "framerate": 4,
                "down": load_animation("warrior", 8, 6),
                "up": load_animation("warrior", 9, 6),
                "left": load_animation("warrior", 10, 6),
                "right": load_animation("warrior", 11, 6)
            }
        }

        self.__index = 0

        self.image = self.__animations[self.__state][self.__direction][self.__index]

        self.rect = self.image.get_rect()

        self.__timer = 0

    def update(self, dt):
        self.__timer += dt

        frametime = 1000 / self.__animations[self.__state]["framerate"]
        while self.__timer >= frametime:
            self.__index = (self.__index + 1) % len(self.__animations[self.__state][self.__direction])
            self.__timer -= frametime

        self.image = self.__animations[self.__state][self.__direction][self.__index]
