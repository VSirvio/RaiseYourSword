import unittest

from sprites.player import Player
from utils import load_animation

class TestPlayer(unittest.TestCase):
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

    def test_idle_animation_is_played_when_player_is_idle(self):
        for direction in ("down", "up", "left", "right"):
            player = Player(self.animations)

            # First, turn player to the correct direction by activating walking to that direction
            # and then stopping walking
            if direction in ("down", "up"):
                player.walk(vert_direction=direction, horiz_direction=None)
            else:
                player.walk(vert_direction=None, horiz_direction=direction)
            player.walk(vert_direction=None, horiz_direction=None)

            # Test frame 0 again in the end to check that the animation loops correctly
            for frame in list(range(len(self.animations["idle"][direction]))) + [0]:
                with self.subTest(direction=direction, frame=frame):
                    self.assertEqual(player.image, self.animations["idle"][direction][frame])
                player.update(dt=1000/self.animations["idle"]["framerate"])

    def test_walking_moves_player_to_the_correct_direction(self):
        for vert_direction in (None, "up", "down"):
            for horiz_direction in (None, "left", "right"):
                player = Player(self.animations)
                starting_position = {"x": player.rect.x, "y": player.rect.y}

                player.walk(vert_direction, horiz_direction)
                player.update(dt=1000)

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
