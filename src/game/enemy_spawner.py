import os
from random import randint

from animation.utils import load_animation
from .character_creation import create_enemy
from .config import (
    DISPLAY_WIDTH,
    DISPLAY_HEIGHT,
    ENEMY_MAX_TIME_BETWEEN_SPAWNING_A_GROUP,
    ENEMY_MAX_TIME_BETWEEN_SPAWNING_ONE,
    ENEMY_MIN_TIME_BETWEEN_SPAWNING_A_GROUP,
    ENEMY_MIN_TIME_BETWEEN_SPAWNING_ONE,
    NUMBER_OF_ENEMIES_TO_SPAWN_AT_ONCE,
    TOTAL_NUMBER_OF_ENEMIES_TO_SPAWN
)

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

    def __pick_random_spawning_position(self):
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

        return spawning_position

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

            new_enemy = create_enemy(
                self.__pick_random_spawning_position(),
                self.__enemy_animation
            )

            if game.another_character_overlaps_with(new_enemy):
                tries += 1
                continue

            game.add_enemy(new_enemy)

            self.__number_of_enemies_to_still_spawn -= 1
            self.__number_of_enemies_waiting_for_spawning -= 1
            tries = 0
