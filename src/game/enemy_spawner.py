import os
from random import randint

from animation.utils import load_animation
from .character_creation import create_enemy

dirname = os.path.dirname(__file__)

class EnemySpawner:
    def __init__(self, game):
        config = game.config.spawning

        self.__enemy_animation = load_animation(
            os.path.join(dirname, "..", "assets", "character_skeleton_animations.yaml")
        )

        self.__group_spawning_timer = 0
        self.__single_spawning_timer = 0
        self.__time_until_next_group_spawn = 0
        self.__time_until_next_single_spawn = randint(
            config.time_between_spawning_one.minimum,
            config.time_between_spawning_one.maximum
        )
        self.__number_of_enemies_to_still_spawn = config.total_number_of_enemies_to_spawn
        self.__number_of_enemies_waiting_for_spawning = 0

    def __pick_random_spawning_position(self, display_width, display_height):
        spawn_area_width = display_width + self.__enemy_animation.frame_width
        spawn_area_height = display_height + self.__enemy_animation.frame_height

        random_number = randint(1, 2 * spawn_area_width + 2 * spawn_area_height)
        if random_number < spawn_area_width:
            spawning_position = (
                -self.__enemy_animation.frame_width + random_number,
                -self.__enemy_animation.frame_height
            )
        elif random_number < 2 * spawn_area_width:
            spawning_position = (
                -self.__enemy_animation.frame_width + random_number - spawn_area_width,
                display_height
            )
        elif random_number < 2 * spawn_area_width + spawn_area_height:
            spawning_position = (
                -self.__enemy_animation.frame_width,
                -self.__enemy_animation.frame_height + random_number - 2 * spawn_area_width
            )
        else:
            spawning_position = (
                display_width,
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
                self.__number_of_enemies_waiting_for_spawning +
                    game.config.spawning.number_of_enemies_to_spawn_at_once,
                self.__number_of_enemies_to_still_spawn,
                1000
            )

            self.__group_spawning_timer -= self.__time_until_next_group_spawn
            self.__time_until_next_group_spawn = randint(
                game.config.spawning.time_between_spawning_a_group.minimum,
                game.config.spawning.time_between_spawning_a_group.maximum
            )

        tries = 0
        while self.__single_spawning_timer >= self.__time_until_next_single_spawn:
            self.__single_spawning_timer -= self.__time_until_next_single_spawn
            self.__time_until_next_single_spawn = randint(
                game.config.spawning.time_between_spawning_one.minimum,
                game.config.spawning.time_between_spawning_one.maximum
            )

            if self.__number_of_enemies_waiting_for_spawning <= 0 or tries >= 5:
                continue

            new_enemy = create_enemy(
                self.__pick_random_spawning_position(
                    game.config.graphics.display_width,
                    game.config.graphics.display_height
                ),
                self.__enemy_animation,
                game.config.ai
            )

            if game.another_character_overlaps_with(new_enemy):
                tries += 1
                continue

            game.add_enemy(new_enemy)

            self.__number_of_enemies_to_still_spawn -= 1
            self.__number_of_enemies_waiting_for_spawning -= 1
            tries = 0
