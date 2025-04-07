import pygame
import unittest

from sprites.player import Player
from utils import load_animation, vert_and_horiz_components_from


class StubEnemy:
    def __init__(self, bounding_box):
        self.__bounding_box = bounding_box

    @property
    def bounding_box(self):
        return self.__bounding_box


class TestPlayer(unittest.TestCase):
    def __turn_to_direction(self, player, direction):
        # Turn player to the given direction by activating walking to that direction and then
        # stopping walking
        player.walk(*vert_and_horiz_components_from(direction))
        player.walk(vert_direction=None, horiz_direction=None)

    def setUp(self):
        self.animations = {
            "idle": {
                "framerate": 4,
                "down": load_animation("warrior", 0, 5),
                "up": load_animation("warrior", 1, 5),
                "left": load_animation("warrior", 2, 5),
                "right": load_animation("warrior", 3, 5)
            },
            "walk": {
                "framerate": 12,
                "down": load_animation("warrior", 4, 8),
                "up": load_animation("warrior", 5, 8),
                "left": load_animation("warrior", 6, 8),
                "right": load_animation("warrior", 7, 8)
            },
            "attack": {
                "framerate": 15,
                "down": load_animation("warrior", 8, 6),
                "up": load_animation("warrior", 9, 6),
                "left": load_animation("warrior", 10, 6),
                "right": load_animation("warrior", 11, 6)
            }
        }
        self.enemy = StubEnemy(bounding_box=pygame.Rect(0, 0, 0, 0))

    def test_idle_animation_is_played_when_player_is_idle(self):
        for direction in ("down", "up", "left", "right"):
            player = Player(self.animations)
            self.__turn_to_direction(player, direction)

            # Test frame 0 again in the end to check that the animation loops correctly
            for frame in list(range(len(self.animations["idle"][direction]))) + [0]:
                with self.subTest(direction=direction, frame=frame):
                    self.assertEqual(player.image, self.animations["idle"][direction][frame])
                player.update(dt=1000/self.animations["idle"]["framerate"], enemy=self.enemy)

    def test_walking_moves_player_to_the_correct_direction(self):
        for vert_direction in (None, "up", "down"):
            for horiz_direction in (None, "left", "right"):
                player = Player(self.animations)
                starting_position = {"x": player.rect.x, "y": player.rect.y}

                player.walk(vert_direction, horiz_direction)
                player.update(dt=1000, enemy=self.enemy)

                with self.subTest(vert_direction=vert_direction, horiz_direction=horiz_direction):
                    if vert_direction == "up":
                        self.assertLess(player.rect.y, starting_position["y"])
                    elif vert_direction == "down":
                        self.assertGreater(player.rect.y, starting_position["y"])
                    else:
                        self.assertEqual(player.rect.y, starting_position["y"])

                    if horiz_direction == "left":
                        self.assertLess(player.rect.x, starting_position["x"])
                    elif horiz_direction == "right":
                        self.assertGreater(player.rect.x, starting_position["x"])
                    else:
                        self.assertEqual(player.rect.x, starting_position["x"])

    def test_attack_animation_is_played_when_player_attacks(self):
        for direction in ("down", "up", "left", "right"):
            player = Player(self.animations)
            self.__turn_to_direction(player, direction)

            player.attack(self.enemy)

            for frame in range(len(self.animations["attack"][direction])):
                with self.subTest(direction=direction, frame=frame):
                    self.assertEqual(player.image, self.animations["attack"][direction][frame])
                player.update(dt=1000/self.animations["attack"]["framerate"], enemy=self.enemy)

    def test_player_cannot_move_while_attacking(self):
        for attack_direction in ("down", "up", "left", "right"):
            for walk_direction in ("down", "up", "left", "right"):
                player = Player(self.animations)
                starting_position = {"x": player.rect.x, "y": player.rect.y}

                self.__turn_to_direction(player, attack_direction)
                player.attack(self.enemy)

                player.walk(*vert_and_horiz_components_from(walk_direction))

                attack_frame_count = len(self.animations["attack"][attack_direction])
                attack_single_frame_duration = 1000 / self.animations["attack"]["framerate"]
                attack_total_duration = attack_frame_count * attack_single_frame_duration
                player.update(dt=attack_total_duration-1, enemy=self.enemy)

                with self.subTest(attack_direction=attack_direction, walk_direction=walk_direction):
                    self.assertEqual(player.rect.x, starting_position["x"])
                    self.assertEqual(player.rect.y, starting_position["y"])
