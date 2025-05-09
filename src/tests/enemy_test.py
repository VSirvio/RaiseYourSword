from math import ceil
import os
import unittest

import pygame

from animation.utils import load_animation
from game.character_creation import create_enemy
from game.config import ENEMY_AI_IDLE_TIME_MAX, ENEMY_AI_WALK_TIME_MAX

dirname = os.path.dirname(__file__)


class StubPlayer:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def bounding_box(self):
        return pygame.Rect(0, 0, 0, 0)

    @property
    def state(self):
        return "idle"


class TestEnemy(unittest.TestCase):
    def setUp(self):
        self.starting_position = (200, 27)

        self.animation = load_animation(
            os.path.join(dirname, "..", "assets", "character_skeleton_animations.yaml")
        )

        self.player = StubPlayer(x=0, y=0)

    def test_enemy_moves(self):
        enemy = create_enemy(self.starting_position, self.animation)

        for _ in range(0, ceil((ENEMY_AI_IDLE_TIME_MAX + ENEMY_AI_WALK_TIME_MAX) * 60 / 1000)):
            enemy.update(dt=ceil(1000/60), opponents=[self.player], other_characters=[])

        self.assertNotEqual((enemy.x, enemy.y), self.starting_position)
