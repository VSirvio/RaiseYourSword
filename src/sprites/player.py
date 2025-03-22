import pygame

from config import GRAPHICS_SCALING_FACTOR
from utils import load_animation

WALKING_SPEED = 60

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
                "framerate": 12,
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

        self.__walk_timer = 0

    def update(self, dt):
        self.__timer += dt
        self.__walk_timer += dt

        frametime = 1000 / self.__animations[self.__state]["framerate"]
        while self.__timer >= frametime:
            self.__index = (self.__index + 1) % len(self.__animations[self.__state][self.__direction])
            self.__timer -= frametime

        self.image = self.__animations[self.__state][self.__direction][self.__index]

        dx = dy = 0
        if self.__state == "walk":
            if self.__direction == "down":
                dy = 1
            elif self.__direction == "up":
                dy = -1
            elif self.__direction == "left":
                dx = -1
            elif self.__direction == "right":
                dx = 1

            time_per_px = 1000 / WALKING_SPEED
            while self.__walk_timer >= time_per_px:
                self.rect.x += GRAPHICS_SCALING_FACTOR * dx
                self.rect.y += GRAPHICS_SCALING_FACTOR * dy
                self.__walk_timer -= time_per_px

    def walk(self, direction):
        self.__state = "walk"
        self.__direction = direction
        self.__index = 0
        self.image = self.__animations[self.__state][self.__direction][self.__index]
        self.__timer = 0
        self.__walk_timer = 0

    def stop(self):
        self.__state = "idle"
        self.__index = 0
        self.image = self.__animations[self.__state][self.__direction][self.__index]
        self.__timer = 0
