import unittest

from direction import direction
from direction.direction import Direction, HorizontalDirection, VerticalDirection

class TestDirection(unittest.TestCase):
    def test_equality_is_determined_correctly(self):
        self.assertEqual(
            Direction(VerticalDirection.NONE, HorizontalDirection.NONE),
            Direction(VerticalDirection.NONE, HorizontalDirection.NONE)
        )
        self.assertEqual(
            Direction(VerticalDirection.DOWN, HorizontalDirection.NONE),
            Direction(VerticalDirection.DOWN, HorizontalDirection.NONE)
        )
        self.assertEqual(
            Direction(VerticalDirection.UP, HorizontalDirection.RIGHT),
            Direction(VerticalDirection.UP, HorizontalDirection.RIGHT)
        )

        self.assertNotEqual(direction.NONE, direction.DOWN_LEFT)
        self.assertNotEqual(direction.UP_RIGHT, direction.RIGHT)
        self.assertNotEqual(direction.UP, direction.DOWN)

    def test_forming_movement_vectors(self):
        self.assertEqual(direction.NONE.movement_vector, (0, 0))
        self.assertEqual(direction.UP.movement_vector, (0, -1))
        self.assertEqual(direction.DOWN_RIGHT.movement_vector, (1, 1))

    def test_clipping_to_four_directions(self):
        self.assertEqual(direction.NONE.clip_to_four_directions(), direction.NONE)
        self.assertEqual(direction.RIGHT.clip_to_four_directions(), direction.RIGHT)
        self.assertEqual(direction.UP_LEFT.clip_to_four_directions(), direction.LEFT)
