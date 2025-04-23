import pygame
import unittest

import direction
from direction import HorizontalDirection, VerticalDirection, NONE, DOWN, UP, LEFT, RIGHT
import events
from sprites.player import Player
from utils import load_animation


class StubEnemy:
    def __init__(self, bounding_box):
        self.__bounding_box = bounding_box

    @property
    def bounding_box(self):
        return self.__bounding_box


class TestPlayer(unittest.TestCase):
    def setUp(self):
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
                DOWN: load_animation("warrior", 8, 6),
                UP: load_animation("warrior", 9, 6),
                LEFT: load_animation("warrior", 10, 6),
                RIGHT: load_animation("warrior", 11, 6)
            }
        }
        self.bounding_box = pygame.Rect((11, 6), (25, 36))
        self.weapon_hitbox = {
            DOWN: pygame.Rect((0, 24), (48, 24)),
            UP: pygame.Rect((0, 0), (48, 24)),
            LEFT: pygame.Rect((0, 0), (24, 48)),
            RIGHT: pygame.Rect((24, 0), (24, 48))
        }
        self.starting_position = ((260 - 48) // 2, (190 - 48) // 2 - 7)
        self.walking_speed = 75

        self.enemy = StubEnemy(bounding_box=pygame.Rect(0, 0, 0, 0))
        self.__walk_direction = NONE

    def __turn_to_direction(self, player, new_direction):
        # Turn player to the given direction by activating walking to that direction and then
        # stopping walking
        player.handle_event(events.MovementDirectionChanged(new_direction), None)
        player.handle_event(events.MovementDirectionChanged(NONE), None)
        self.__walk_direction = NONE

    def __walk_to_direction(self, player, direction):
        self.__walk_direction = direction
        player.handle_event(events.MovementDirectionChanged(self.__walk_direction), None)

    def __attack_an_enemy(self, player, enemy):
        player.handle_event(events.AttackStarted(), enemy)

    def test_idle_animation_is_played_when_player_is_idle(self):
        for direction in (DOWN, UP, LEFT, RIGHT):
            player = Player(
                self.animations, self.bounding_box, self.weapon_hitbox, self.starting_position,
                self.walking_speed
            )
            self.__turn_to_direction(player, direction)

            # Test frame 0 again in the end to check that the animation loops correctly
            for frame in list(range(len(self.animations["idle"][direction]))) + [0]:
                with self.subTest(direction=direction, frame=frame):
                    self.assertEqual(player.image, self.animations["idle"][direction][frame])
                player.update(dt=1000/self.animations["idle"]["framerate"], enemy=self.enemy)

    def test_walking_moves_player_to_the_correct_direction(self):
        for walk_direction in direction.ALL:
            player = Player(
                self.animations, self.bounding_box, self.weapon_hitbox, self.starting_position,
                self.walking_speed
            )
            starting_position = {"x": player.rect.x, "y": player.rect.y}

            self.__walk_to_direction(player, walk_direction)
            player.update(dt=1000, enemy=self.enemy)

            with self.subTest(direction=walk_direction):
                if walk_direction.vertical_component == VerticalDirection.UP:
                    self.assertLess(player.rect.y, starting_position["y"])
                elif walk_direction.vertical_component == VerticalDirection.DOWN:
                    self.assertGreater(player.rect.y, starting_position["y"])
                else:
                    self.assertEqual(player.rect.y, starting_position["y"])

                if walk_direction.horizontal_component == HorizontalDirection.LEFT:
                    self.assertLess(player.rect.x, starting_position["x"])
                elif walk_direction.horizontal_component == HorizontalDirection.RIGHT:
                    self.assertGreater(player.rect.x, starting_position["x"])
                else:
                    self.assertEqual(player.rect.x, starting_position["x"])

    def test_attack_animation_is_played_when_player_attacks(self):
        for direction in (DOWN, UP, LEFT, RIGHT):
            player = Player(
                self.animations, self.bounding_box, self.weapon_hitbox, self.starting_position,
                self.walking_speed
            )
            self.__turn_to_direction(player, direction)

            self.__attack_an_enemy(player, self.enemy)

            for frame in range(len(self.animations["attack"][direction])):
                with self.subTest(direction=direction, frame=frame):
                    self.assertEqual(player.image, self.animations["attack"][direction][frame])
                player.update(dt=1000/self.animations["attack"]["framerate"], enemy=self.enemy)

    def test_player_cannot_move_while_attacking(self):
        for attack_direction in (DOWN, UP, LEFT, RIGHT):
            for walk_direction in (DOWN, UP, LEFT, RIGHT):
                player = Player(
                    self.animations, self.bounding_box, self.weapon_hitbox, self.starting_position,
                    self.walking_speed
                )
                starting_position = {"x": player.rect.x, "y": player.rect.y}

                self.__turn_to_direction(player, attack_direction)
                self.__attack_an_enemy(player, self.enemy)

                self.__walk_to_direction(player, walk_direction)

                attack_frame_count = len(self.animations["attack"][attack_direction])
                attack_single_frame_duration = 1000 / self.animations["attack"]["framerate"]
                attack_total_duration = attack_frame_count * attack_single_frame_duration
                player.update(dt=attack_total_duration-1, enemy=self.enemy)

                with self.subTest(attack_direction=attack_direction, walk_direction=walk_direction):
                    self.assertEqual(player.rect.x, starting_position["x"])
                    self.assertEqual(player.rect.y, starting_position["y"])
