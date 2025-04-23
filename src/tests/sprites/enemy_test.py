from math import ceil

import pygame
import unittest

from config import ENEMY_AI_IDLE_TIME_MAX, ENEMY_AI_WALK_TIME_MAX
from direction import DOWN, UP, LEFT, RIGHT
from sprites.enemy import Enemy
from utils import load_animation


class StubPlayer:
    def __init__(self, rect):
        self.__rect = rect

    @property
    def rect(self):
        return self.__rect


class TestEnemy(unittest.TestCase):
    def setUp(self):
        self.animations = {
            "idle": {
                "framerate": 4,
                DOWN: load_animation("skeleton", 0, 6),
                UP: load_animation("skeleton", 1, 6),
                LEFT: load_animation("skeleton", 2, 6),
                RIGHT: load_animation("skeleton", 3, 6)
            },
            "walk": {
                "framerate": 12,
                DOWN: load_animation("skeleton", 4, 6),
                UP: load_animation("skeleton", 5, 6),
                LEFT: load_animation("skeleton", 6, 6),
                RIGHT: load_animation("skeleton", 7, 6)
            },
            "attack": {
                "framerate": 10,
                DOWN: load_animation("skeleton", 8, 8),
                UP: load_animation("skeleton", 9, 8),
                LEFT: load_animation("skeleton", 10, 8),
                RIGHT: load_animation("skeleton", 11, 8)
            }
        }
        self.bounding_box = pygame.Rect((20, 22), (8, 11))
        self.weapon_hitbox = {
            DOWN: pygame.Rect((0, 26), (48, 22)),
            UP: pygame.Rect((0, 0), (48, 22)),
            LEFT: pygame.Rect((0, 0), (22, 48)),
            RIGHT: pygame.Rect((26, 0), (22, 48))
        }
        self.starting_position = (200, 27)
        self.player = StubPlayer(rect=pygame.Rect(0, 0, 0, 0))

    def test_enemy_moves(self):
        enemy = Enemy(
            self.animations, self.bounding_box, self.weapon_hitbox, self.starting_position
        )
        starting_position = (enemy.rect.x, enemy.rect.y)

        for frame in range(0, ceil((ENEMY_AI_IDLE_TIME_MAX + ENEMY_AI_WALK_TIME_MAX) * 60 / 1000)):
            enemy.update(dt=ceil(1000/60), player=self.player)

        self.assertNotEqual((enemy.rect.x, enemy.rect.y), starting_position)
