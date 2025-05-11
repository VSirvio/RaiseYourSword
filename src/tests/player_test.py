import os
import unittest

import pygame

from animation.utils import load_animation
from config import generate_configuration
from direction import direction
from direction.direction import HorizontalDirection, VerticalDirection, NONE, DOWN, UP, LEFT, RIGHT
from game import events
from game.character_creation import create_player

dirname = os.path.dirname(__file__)


class TestPlayer(unittest.TestCase):
    def setUp(self):
        config = generate_configuration()

        self.starting_pos = (
            (config.graphics.display_width - 48) // 2,
            (config.graphics.display_height - 48) // 2 - 7
        )
        self.animations = load_animation(
            os.path.join(dirname, "..", "assets", "character_warrior_animations.yaml")
        )
        self.game_area_bounds = pygame.Rect(5, 7, 251, 180)

        self.enemies = []
        self.__walk_direction = NONE

    def __turn_to_direction(self, player, new_direction):
        # Turn player to the given direction by activating walking to that direction and then
        # stopping walking
        player.handle_event(events.MovementDirectionChanged(new_direction), None)
        player.handle_event(events.MovementDirectionChanged(NONE), None)
        self.__walk_direction = NONE

    def __walk_to_direction(self, player, walking_direction):
        self.__walk_direction = walking_direction
        player.handle_event(events.MovementDirectionChanged(self.__walk_direction), None)

    def __attack_an_enemy(self, player, enemies):
        player.handle_event(events.AttackStarted(), enemies)

    def test_idle_animation_is_played_when_player_is_idle(self):
        for direction_facing in (DOWN, UP, LEFT, RIGHT):
            player = create_player(self.starting_pos, self.animations, self.game_area_bounds)
            self.__turn_to_direction(player, direction_facing)

            # Test frame 0 again in the end to check that the animation loops correctly
            for frame in list(range(len(self.animations["idle"][direction_facing].frames))) + [0]:
                with self.subTest(direction=direction_facing, frame=frame):
                    self.assertEqual(
                        player.sprite.image,
                        self.animations["idle"][direction_facing].frames[frame]
                    )
                player.update(
                    dt=1000/self.animations["idle"][direction_facing].framerate,
                    opponents=self.enemies, other_characters=[]
                )

    def test_walking_moves_player_to_the_correct_direction(self):
        for walk_direction in direction.ALL:
            player = create_player(self.starting_pos, self.animations, self.game_area_bounds)
            starting_position = {"x": player.x, "y": player.y}

            self.__walk_to_direction(player, walk_direction)
            player.update(dt=1000, opponents=self.enemies, other_characters=[])

            with self.subTest(direction=walk_direction):
                if walk_direction.vertical_component == VerticalDirection.UP:
                    self.assertLess(player.y, starting_position["y"])
                elif walk_direction.vertical_component == VerticalDirection.DOWN:
                    self.assertGreater(player.y, starting_position["y"])
                else:
                    self.assertEqual(player.y, starting_position["y"])

                if walk_direction.horizontal_component == HorizontalDirection.LEFT:
                    self.assertLess(player.x, starting_position["x"])
                elif walk_direction.horizontal_component == HorizontalDirection.RIGHT:
                    self.assertGreater(player.x, starting_position["x"])
                else:
                    self.assertEqual(player.x, starting_position["x"])

    def test_attack_animation_is_played_when_player_attacks(self):
        for direction_facing in (DOWN, UP, LEFT, RIGHT):
            player = create_player(self.starting_pos, self.animations, self.game_area_bounds)
            self.__turn_to_direction(player, direction_facing)

            self.__attack_an_enemy(player, self.enemies)

            for frame in range(len(self.animations["attack"][direction_facing].frames)):
                with self.subTest(direction=direction_facing, frame=frame):
                    self.assertEqual(
                        player.sprite.image,
                        self.animations["attack"][direction_facing].frames[frame]
                    )
                player.update(
                    dt=1000/self.animations["attack"][direction_facing].framerate,
                    opponents=self.enemies, other_characters=[]
                )

    def test_player_cannot_move_while_attacking(self):
        for attack_direction in (DOWN, UP, LEFT, RIGHT):
            for walk_direction in (DOWN, UP, LEFT, RIGHT):
                player = create_player(self.starting_pos, self.animations, self.game_area_bounds)
                starting_position = {"x": player.x, "y": player.y}

                self.__turn_to_direction(player, attack_direction)
                self.__attack_an_enemy(player, self.enemies)

                self.__walk_to_direction(player, walk_direction)

                current_animation = self.animations["attack"][attack_direction]
                attack_frame_count = len(current_animation.frames)
                attack_single_frame_duration = 1000 / current_animation.framerate
                attack_total_duration = attack_frame_count * attack_single_frame_duration
                player.update(
                    dt=attack_total_duration-1, opponents=self.enemies, other_characters=[]
                )

                with self.subTest(attack_direction=attack_direction, walk_direction=walk_direction):
                    self.assertEqual(player.x, starting_position["x"])
                    self.assertEqual(player.y, starting_position["y"])

    def test_player_cannot_walk_out_of_the_game_area(self):
        for walk_direction in (DOWN, UP, LEFT, RIGHT):
            player = create_player(self.starting_pos, self.animations, self.game_area_bounds)

            self.__walk_to_direction(player, walk_direction)
            for _ in range(30*60):
                player.update(dt=1000/60, opponents=[], other_characters=[])

            with self.subTest(direction=walk_direction):
                self.assertGreaterEqual(player.bounding_box.left, self.game_area_bounds.left)
                self.assertLessEqual(player.bounding_box.right, self.game_area_bounds.right)

                self.assertGreaterEqual(player.bounding_box.top, self.game_area_bounds.top)
                self.assertLessEqual(player.bounding_box.bottom, self.game_area_bounds.bottom)
