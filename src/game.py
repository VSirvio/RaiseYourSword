import pygame

from sprites.background import Background
from sprites.enemy import Enemy
from sprites.player import Player
from utils import load_animation

class Game:
    def __init__(self):
        self.__background = Background()
        self.__player = Player({
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
                "framerate": 15,
                "down": load_animation("warrior", 8, 6),
                "up": load_animation("warrior", 9, 6),
                "left": load_animation("warrior", 10, 6),
                "right": load_animation("warrior", 11, 6)
            }
        })
        self.__enemy = Enemy({
            "idle": {
                "framerate": 4,
                "down": load_animation("skeleton", 0, 6),
                "up": load_animation("skeleton", 1, 6),
                "left": load_animation("skeleton", 2, 6),
                "right": load_animation("skeleton", 3, 6)
            },
            "walk": {
                "framerate": 12,
                "down": load_animation("skeleton", 4, 6),
                "up": load_animation("skeleton", 5, 6),
                "left": load_animation("skeleton", 6, 6),
                "right": load_animation("skeleton", 7, 6)
            },
            "attack": {
                "framerate": 15,
                "down": load_animation("skeleton", 8, 8),
                "up": load_animation("skeleton", 9, 8),
                "left": load_animation("skeleton", 10, 8),
                "right": load_animation("skeleton", 11, 8)
            }
        })
        self.__all_sprites = pygame.sprite.Group(self.__background, self.__player, self.__enemy)

    def draw(self, surface):
        self.__all_sprites.draw(surface)

    def update(self, dt):
        self.__all_sprites.update(dt)

    def walk(self, vert_direction, horiz_direction):
        self.__player.walk(vert_direction, horiz_direction)

    def attack(self):
        self.__player.attack()
