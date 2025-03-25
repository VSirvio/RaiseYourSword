import unittest

from sprites.player import Player

class TestPlayer(unittest.TestCase):
    def test_walking_moves_player_to_the_correct_direction(self):
        for vert_direction in (None, "up", "down"):
            for horiz_direction in (None, "left", "right"):
                player = Player()
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
