from math import ceil
import os
import unittest

import pygame

from animation.utils import load_animation
from config import generate_configuration
from game.character_creation import create_enemy

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
        self.config = generate_configuration()
        self.max_idle_time = self.config.ai.idle_time.maximum
        self.max_walk_time = self.config.ai.walk_time.maximum

        self.starting_position = (200, 27)

        self.animation = load_animation(
            os.path.join(dirname, "..", "assets", "character_skeleton_animations.yaml")
        )

        self.player = StubPlayer(x=0, y=0)

    def test_enemy_moves(self):
        enemy = create_enemy(self.starting_position, self.animation, self.config.ai)

        for _ in range(0, ceil((self.max_idle_time + self.max_walk_time) * 60 / 1000)):
            enemy.update(dt=ceil(1000/60), opponents=[self.player], other_characters=[],
                config=self.config.ai)

        self.assertNotEqual((enemy.x, enemy.y), self.starting_position)
