import unittest

import pygame

from character import Character
from components.animations_component import AnimationsComponent
from components.player_physics import PlayerPhysics
import direction
from direction import HorizontalDirection, VerticalDirection, NONE, DOWN, UP, LEFT, RIGHT
import events
from player_direction import PlayerDirection
import states.idle_state
from utils import load_animation


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.initial_state = states.idle_state.IdleState()
        self.starting_position = ((260 - 48) // 2, (190 - 48) // 2 - 7)
        self.direction = PlayerDirection(facing=DOWN, moving=NONE, controlled_toward=NONE)
        self.animations = {
            "idle": {
                "framerate": 4,
                DOWN: load_animation("warrior", 0, 5),
                UP: load_animation("warrior", 1, 5),
                LEFT: load_animation("warrior", 2, 5),
                RIGHT: load_animation("warrior", 3, 5)
            },
            "walk": {
                "framerate": 12,
                DOWN: load_animation("warrior", 4, 8),
                UP: load_animation("warrior", 5, 8),
                LEFT: load_animation("warrior", 6, 8),
                RIGHT: load_animation("warrior", 7, 8)
            },
            "attack": {
                "framerate": 15,
                "damage_frames": [],
                DOWN: load_animation("warrior", 8, 6),
                UP: load_animation("warrior", 9, 6),
                LEFT: load_animation("warrior", 10, 6),
                RIGHT: load_animation("warrior", 11, 6)
            }
        }
        self.physics = PlayerPhysics(
            walking_speed=75,
            bounding_box=pygame.Rect((11, 6), (25, 36)),
            weapon_hitbox={
                DOWN: pygame.Rect((0, 24), (48, 24)),
                UP: pygame.Rect((0, 0), (48, 24)),
                LEFT: pygame.Rect((0, 0), (24, 48)),
                RIGHT: pygame.Rect((24, 0), (24, 48))
            },
            game_area_size=(260, 190)
        )

        self.enemies = []
        self.__walk_direction = NONE

    def __create_new_player(self):
        return Character(
            role="player", initial_state=self.initial_state,
            starting_position=self.starting_position, direction=self.direction,
            animations=AnimationsComponent(self.animations), physics=self.physics
        )

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
            player = self.__create_new_player()
            self.__turn_to_direction(player, direction_facing)

            # Test frame 0 again in the end to check that the animation loops correctly
            for frame in list(range(len(self.animations["idle"][direction_facing]))) + [0]:
                with self.subTest(direction=direction_facing, frame=frame):
                    self.assertEqual(
                        player.sprite.image,
                        self.animations["idle"][direction_facing][frame]
                    )
                player.update(
                    dt=1000/self.animations["idle"]["framerate"],
                    opponents_to={"player": self.enemies}
                )

    def test_walking_moves_player_to_the_correct_direction(self):
        for walk_direction in direction.ALL:
            player = self.__create_new_player()
            starting_position = {"x": player.x, "y": player.y}

            self.__walk_to_direction(player, walk_direction)
            player.update(dt=1000, opponents_to={"player": self.enemies})

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
            player = self.__create_new_player()
            self.__turn_to_direction(player, direction_facing)

            self.__attack_an_enemy(player, self.enemies)

            for frame in range(len(self.animations["attack"][direction_facing])):
                with self.subTest(direction=direction_facing, frame=frame):
                    self.assertEqual(
                        player.sprite.image,
                        self.animations["attack"][direction_facing][frame]
                    )
                player.update(
                    dt=1000/self.animations["attack"]["framerate"],
                    opponents_to={"player": self.enemies}
                )

    def test_player_cannot_move_while_attacking(self):
        for attack_direction in (DOWN, UP, LEFT, RIGHT):
            for walk_direction in (DOWN, UP, LEFT, RIGHT):
                player = self.__create_new_player()
                starting_position = {"x": player.x, "y": player.y}

                self.__turn_to_direction(player, attack_direction)
                self.__attack_an_enemy(player, self.enemies)

                self.__walk_to_direction(player, walk_direction)

                attack_frame_count = len(self.animations["attack"][attack_direction])
                attack_single_frame_duration = 1000 / self.animations["attack"]["framerate"]
                attack_total_duration = attack_frame_count * attack_single_frame_duration
                player.update(dt=attack_total_duration-1, opponents_to={"player": self.enemies})

                with self.subTest(attack_direction=attack_direction, walk_direction=walk_direction):
                    self.assertEqual(player.x, starting_position["x"])
                    self.assertEqual(player.y, starting_position["y"])
