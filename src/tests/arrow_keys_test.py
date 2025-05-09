import unittest

import pygame

from direction import direction
from game.arrow_keys import ArrowKeys


class StubEvent:
    def __init__(self, event_type, key):
        self.__type = event_type
        self.__key = key

    @property
    def type(self):
        return self.__type

    @property
    def key(self):
        return self.__key


class TestArrowKeys(unittest.TestCase):
    def setUp(self):
        self.correct_directions = {
            pygame.K_DOWN: direction.DOWN,
            pygame.K_UP: direction.UP,
            pygame.K_LEFT: direction.LEFT,
            pygame.K_RIGHT: direction.RIGHT
        }

    def test_current_direction_is_none_by_default(self):
        arrow_keys = ArrowKeys()
        self.assertEqual(arrow_keys.current_direction, direction.NONE)

    def test_key_down_event_sets_current_direction_correctly(self):
        for key in self.correct_directions:
            arrow_keys = ArrowKeys()

            arrow_keys.handle(StubEvent(pygame.KEYDOWN, key))

            with self.subTest(key=key):
                self.assertEqual(arrow_keys.current_direction, self.correct_directions[key])

    def test_all_keys_are_released_correctly(self):
        for key in self.correct_directions:
            arrow_keys = ArrowKeys()

            arrow_keys.handle(StubEvent(pygame.KEYDOWN, key))

            arrow_keys.release_all()

            with self.subTest(key=key):
                self.assertEqual(arrow_keys.current_direction, direction.NONE)
