import os
from random import randint

import pygame

from animation.utils import load_animation
from components.animations_component import AnimationsComponent
from components.physics_component import PhysicsComponent
from direction.character_direction import CharacterDirection
from direction.direction import DOWN, LEFT, NONE, RIGHT, UP
from game.character import Character
from game.config import (
    DISPLAY_WIDTH,
    DISPLAY_HEIGHT,
    ENEMY_MAX_TIME_BETWEEN_SPAWNING_A_GROUP,
    ENEMY_MAX_TIME_BETWEEN_SPAWNING_ONE,
    ENEMY_MIN_TIME_BETWEEN_SPAWNING_A_GROUP,
    ENEMY_MIN_TIME_BETWEEN_SPAWNING_ONE,
    ENEMY_WALKING_SPEED,
    NUMBER_OF_ENEMIES_TO_SPAWN_AT_ONCE,
    TOTAL_NUMBER_OF_ENEMIES_TO_SPAWN
)
import states.ai.idle_state
import states.game.defeat_screen_state
import states.game.victory_screen_state

dirname = os.path.dirname(__file__)

class EnemySpawner:
    def __init__(self):
        self.__enemy_animation = load_animation(
            os.path.join(dirname, "..", "assets", "character_skeleton_animations.yaml")
        )

        self.__group_spawning_timer = 0
        self.__single_spawning_timer = 0
        self.__time_until_next_group_spawn = 0
        self.__time_until_next_single_spawn = randint(
            ENEMY_MIN_TIME_BETWEEN_SPAWNING_ONE,
            ENEMY_MAX_TIME_BETWEEN_SPAWNING_ONE
        )
        self.__number_of_enemies_to_still_spawn = TOTAL_NUMBER_OF_ENEMIES_TO_SPAWN
        self.__number_of_enemies_waiting_for_spawning = 0

    def __create_enemy(self, starting_position):
        return Character(
            initial_state=states.ai.idle_state.IdleState(),
            starting_position=starting_position,
            direction=CharacterDirection(facing=DOWN, moving=NONE),
            animations=AnimationsComponent(self.__enemy_animation),
            physics=PhysicsComponent(
                walking_speed=ENEMY_WALKING_SPEED,
                bounding_box=pygame.Rect((16, 20), (16, 20)),
                character_hitbox=pygame.Rect((14, 10), (20, 33)),
                weapon_hitbox={
                    DOWN: pygame.Rect((7, 26), (25, 17)),
                    UP: pygame.Rect((16, 5), (25, 16)),
                    LEFT: pygame.Rect((6, 16), (14, 25)),
                    RIGHT: pygame.Rect((29, 14), (14, 27))
                }
            )
        )

    def spawn_enemies(self, dt, game):
        self.__group_spawning_timer += dt
        self.__single_spawning_timer += dt

        while (self.__group_spawning_timer >= self.__time_until_next_group_spawn and
                self.__number_of_enemies_to_still_spawn > 0):
            self.__number_of_enemies_waiting_for_spawning = min(
                self.__number_of_enemies_waiting_for_spawning + NUMBER_OF_ENEMIES_TO_SPAWN_AT_ONCE,
                self.__number_of_enemies_to_still_spawn,
                1000
            )

            self.__group_spawning_timer -= self.__time_until_next_group_spawn
            self.__time_until_next_group_spawn = randint(
                ENEMY_MIN_TIME_BETWEEN_SPAWNING_A_GROUP,
                ENEMY_MAX_TIME_BETWEEN_SPAWNING_A_GROUP
            )

        tries = 0
        while self.__single_spawning_timer >= self.__time_until_next_single_spawn:
            self.__single_spawning_timer -= self.__time_until_next_single_spawn
            self.__time_until_next_single_spawn = randint(
                ENEMY_MIN_TIME_BETWEEN_SPAWNING_ONE,
                ENEMY_MAX_TIME_BETWEEN_SPAWNING_ONE
            )

            if self.__number_of_enemies_waiting_for_spawning <= 0 or tries >= 5:
                continue

            spawn_area_width = DISPLAY_WIDTH + self.__enemy_animation.frame_width
            spawn_area_height = DISPLAY_HEIGHT + self.__enemy_animation.frame_height

            random_number = randint(1, 2 * spawn_area_width + 2 * spawn_area_height)
            if random_number < spawn_area_width:
                spawning_position = (
                    -self.__enemy_animation.frame_width + random_number,
                    -self.__enemy_animation.frame_height
                )
            elif random_number < 2 * spawn_area_width:
                spawning_position = (
                    -self.__enemy_animation.frame_width + random_number - spawn_area_width,
                    DISPLAY_HEIGHT
                )
            elif random_number < 2 * spawn_area_width + spawn_area_height:
                spawning_position = (
                    -self.__enemy_animation.frame_width,
                    -self.__enemy_animation.frame_height + random_number - 2 * spawn_area_width
                )
            else:
                spawning_position = (
                    DISPLAY_WIDTH,
                    -self.__enemy_animation.frame_height + random_number -
                        2 * spawn_area_width - spawn_area_height
                )

            new_enemy = self.__create_enemy(spawning_position)

            if game.another_character_overlaps_with(new_enemy):
                tries += 1
                continue

            game.add_enemy(new_enemy)

            self.__number_of_enemies_to_still_spawn -= 1
            self.__number_of_enemies_waiting_for_spawning -= 1
            tries = 0
