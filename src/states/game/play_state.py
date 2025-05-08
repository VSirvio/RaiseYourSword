from random import randint

import pygame

import ai.idle_state
from character import Character
from character_direction import CharacterDirection
from components.animations_component import AnimationsComponent
from components.physics_component import PhysicsComponent
from config import (
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
from direction import DOWN, LEFT, NONE, RIGHT, UP
import events
import states.game.defeat_screen_state
import states.game.victory_screen_state
from utils import load_animation

class PlayState:
    def __init__(self):
        self.__enemy_animation = load_animation("assets/character_skeleton_animations.yaml")

        self.__group_spawning_timer = 0
        self.__single_spawning_timer = 0
        self.__time_until_next_group_spawn = randint(
            ENEMY_MIN_TIME_BETWEEN_SPAWNING_A_GROUP,
            ENEMY_MAX_TIME_BETWEEN_SPAWNING_A_GROUP
        )
        self.__time_until_next_single_spawn = randint(
            ENEMY_MIN_TIME_BETWEEN_SPAWNING_ONE,
            ENEMY_MAX_TIME_BETWEEN_SPAWNING_ONE
        )
        self.__number_of_enemies_spawned_so_far = 0
        self.__number_of_enemies_waiting_for_spawning = 0

    def draw(self, surface):
        pass

    def update(self, *args):
        dt = args[0]
        game = args[1]

        self.__spawn_enemies(dt, game)

    def handle_event(self, *args):
        event = args[0]
        player = args[1]
        enemies = args[2]

        player.handle_event(event, enemies)

        match event:
            case events.PlayerWon():
                return states.game.victory_screen_state.VictoryScreenState()
            case events.PlayerLost():
                return states.game.defeat_screen_state.DefeatScreenState()

    def __create_enemy(self, starting_position):
        return Character(
            initial_state=ai.idle_state.IdleState(),
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

    def __spawn_enemies(self, dt, game):
        self.__group_spawning_timer += dt
        self.__single_spawning_timer += dt

        while (self.__group_spawning_timer >= self.__time_until_next_group_spawn and
                self.__number_of_enemies_spawned_so_far < TOTAL_NUMBER_OF_ENEMIES_TO_SPAWN):
            self.__number_of_enemies_waiting_for_spawning += NUMBER_OF_ENEMIES_TO_SPAWN_AT_ONCE
            if (self.__number_of_enemies_spawned_so_far +
                    self.__number_of_enemies_waiting_for_spawning >
                    TOTAL_NUMBER_OF_ENEMIES_TO_SPAWN):
                self.__number_of_enemies_waiting_for_spawning = (TOTAL_NUMBER_OF_ENEMIES_TO_SPAWN -
                    self.__number_of_enemies_spawned_so_far)

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

            self.__number_of_enemies_spawned_so_far += 1
            self.__number_of_enemies_waiting_for_spawning -= 1
            tries = 0
