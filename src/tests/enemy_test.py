from math import ceil
import unittest

import pygame

import ai.idle_state
from character import Character
from character_direction import CharacterDirection
from components.animations_component import AnimationsComponent
from components.physics_component import PhysicsComponent
from config import ENEMY_AI_IDLE_TIME_MAX, ENEMY_AI_WALK_TIME_MAX
from direction import NONE, DOWN, UP, LEFT, RIGHT
from utils import load_animation


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
    def has_been_defeated(self):
        return False


class TestEnemy(unittest.TestCase):
    def setUp(self):
        self.initial_state = ai.idle_state.IdleState()
        self.starting_position = (200, 27)
        self.direction = CharacterDirection(facing=DOWN, moving=NONE)
        self.animations = load_animation("assets/character_skeleton_animations.yaml")
        self.physics=PhysicsComponent(
            walking_speed=50,
            bounding_box=pygame.Rect((20, 22), (8, 11)),
            weapon_hitbox={
                DOWN: pygame.Rect((0, 26), (48, 22)),
                UP: pygame.Rect((0, 0), (48, 22)),
                LEFT: pygame.Rect((0, 0), (22, 48)),
                RIGHT: pygame.Rect((26, 0), (22, 48))
            }
        )

        self.player = StubPlayer(x=0, y=0)

    def test_enemy_moves(self):
        enemy = Character(
            role="enemy", initial_state=self.initial_state,
            starting_position=self.starting_position, direction=self.direction,
            animations=AnimationsComponent(self.animations), physics=self.physics
        )
        starting_position = (enemy.x, enemy.y)

        for _ in range(0, ceil((ENEMY_AI_IDLE_TIME_MAX + ENEMY_AI_WALK_TIME_MAX) * 60 / 1000)):
            enemy.update(dt=ceil(1000/60), opponents_to={"enemy": [self.player]})

        self.assertNotEqual((enemy.x, enemy.y), starting_position)
