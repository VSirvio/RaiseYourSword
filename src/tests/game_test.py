import unittest

from config import generate_configuration
from game import events
from game.game import Game


class TestGame(unittest.TestCase):
    def test_a_new_game_is_not_finished(self):
        game = Game(config=generate_configuration(), skip_intro=False)

        self.assertFalse(game.finished)

    def test_starts_in_cinematic_texts_state_when_not_set_to_skip_intro(self):
        game = Game(config=generate_configuration(), skip_intro=False)

        self.assertEqual(game.state, "CinematicTextsState")

    def test_starts_in_play_state_when_set_to_skip_intro(self):
        game = Game(config=generate_configuration(), skip_intro=True)

        self.assertEqual(game.state, "PlayState")

    def test_can_get_past_cinematic_texts(self):
        game = Game(config=generate_configuration(), skip_intro=False)

        for _ in range(4):
            game.handle(events.Accept())

        self.assertEqual(game.state, "PlayState")
