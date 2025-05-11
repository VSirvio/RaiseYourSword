from math import ceil, floor, sqrt
import os
import unittest

import pygame

from animation.utils import load_animation
from config import generate_configuration
from configuration.ai_config import AiConfig
from game.character_creation import create_enemy
from utils import Range

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
        return pygame.Rect((self.x + 16, self.y + 20), (16, 20))

    @property
    def character_hitbox(self):
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

    def test_enemy_walks_toward_player(self):
        directions_to_test = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]

        for walk_direction in directions_to_test:
            starting_pos = (
                (self.config.graphics.display_width - self.animation.frame_width) // 2,
                (self.config.graphics.display_height - self.animation.frame_height) // 2
            )

            ai_config = AiConfig(
                idle_time=Range(0, 0),
                walk_time=Range(500, 500),
                attack_initiation_distance=25
            )

            enemy = create_enemy(
                starting_position=starting_pos,
                animation=self.animation,
                ai_config=ai_config
            )

            distance = 40
            player = StubPlayer(
                x=enemy.x+walk_direction[0]*distance,
                y=enemy.y+walk_direction[1]*distance
            )

            for _ in range(3):
                enemy.update(dt=ceil(1000/60), opponents=[player], other_characters=[],
                    config=ai_config)

            with self.subTest(direction=walk_direction):
                dx = enemy.x - starting_pos[0]
                self.assertEqual(
                    0 if dx == 0 else dx / abs(dx),
                    walk_direction[0]
                )

                dy = enemy.y - starting_pos[1]
                self.assertEqual(
                    0 if dy == 0 else dy / abs(dy),
                    walk_direction[1]
                )

    def test_enemy_attacks_when_close_enough_to_the_player(self):
        for walk_direction in [(1, 0), (0, -1), (-1, 0), (0, 1)]:
            starting_pos = (
                (self.config.graphics.display_width - self.animation.frame_width) // 2,
                (self.config.graphics.display_height - self.animation.frame_height) // 2
            )

            attack_initiation_distance = 25

            ai_config = AiConfig(
                idle_time=Range(0, 0),
                walk_time=Range(60000, 60000),
                attack_initiation_distance=attack_initiation_distance
            )

            enemy = create_enemy(
                starting_position=starting_pos,
                animation=self.animation,
                ai_config=ai_config
            )

            distance = 40
            player = StubPlayer(
                x=enemy.x+walk_direction[0]*distance,
                y=enemy.y+walk_direction[1]*distance
            )

            attacking = False
            for _ in range(30 * 60):
                enemy.update(dt=ceil(1000/60), opponents=[player], other_characters=[],
                    config=ai_config)

                if enemy.state == "attack":
                    attacking = True
                    break

            with self.subTest(direction=walk_direction):
                self.assertTrue(attacking)

                dist_x = player.bounding_box.centerx - enemy.bounding_box.centerx
                dist_y = player.bounding_box.centery - enemy.bounding_box.centery
                self.assertEqual(
                    floor(sqrt(dist_x ** 2 + dist_y ** 2)),
                    attack_initiation_distance
                )
