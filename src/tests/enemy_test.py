from math import ceil
import unittest

import pygame

from animation.utils import load_animation
from components.animations_component import AnimationsComponent
from components.physics_component import PhysicsComponent
from direction.direction import NONE, DOWN, UP, LEFT, RIGHT
from direction.character_direction import CharacterDirection
from game.character import Character
from game.config import ENEMY_AI_IDLE_TIME_MAX, ENEMY_AI_WALK_TIME_MAX
import states.ai.idle_state


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
        self.initial_state = states.ai.idle_state.IdleState()
        self.starting_position = (200, 27)
        self.direction = CharacterDirection(facing=DOWN, moving=NONE)
        self.animations = load_animation("../assets/character_skeleton_animations.yaml")
        self.physics=PhysicsComponent(
            walking_speed=50,
            bounding_box=pygame.Rect((16, 19), (16, 21)),
            character_hitbox=pygame.Rect((14, 10), (20, 33)),
            weapon_hitbox={
                DOWN: pygame.Rect((7, 26), (25, 17)),
                UP: pygame.Rect((16, 5), (25, 16)),
                LEFT: pygame.Rect((6, 16), (14, 25)),
                RIGHT: pygame.Rect((29, 14), (14, 27))
            }

        )

        self.player = StubPlayer(x=0, y=0)

    def test_enemy_moves(self):
        enemy = Character(
            initial_state=self.initial_state, starting_position=self.starting_position,
            direction=self.direction, animations=AnimationsComponent(self.animations),
            physics=self.physics
        )
        starting_position = (enemy.x, enemy.y)

        for _ in range(0, ceil((ENEMY_AI_IDLE_TIME_MAX + ENEMY_AI_WALK_TIME_MAX) * 60 / 1000)):
            enemy.update(dt=ceil(1000/60), opponents=[self.player], other_characters=[])

        self.assertNotEqual((enemy.x, enemy.y), starting_position)
