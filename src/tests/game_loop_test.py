import os
import tempfile
import unittest

import pygame

from animation.utils import load_animation
from configuration.ai_config import AiConfig
from configuration.game_config import GameConfig
from configuration.graphics_config import GraphicsConfig
from configuration.spawning_config import SpawningConfig
from game.character_creation import create_enemy
from game.game import Game
from game.game_loop import GameLoop
from utils import Range

dirname = os.path.dirname(__file__)


class StubClock:
    def tick(self, fps):
        return 1000 / fps


class StubEvent:
    def __init__(self, event_type, key=None):
        self.type = event_type
        self.key = key


class StubEventQueue:
    def __init__(self, events):
        self.__events = events

    def get(self):
        return self.__events.pop(0)


class StubGame:
    def __init__(self):
        self.update_called_count = 0

    def update(self, dt):
        self.update_called_count += 1


class StubRenderer:
    def render(self):
        pass


class TestGameLoop(unittest.TestCase):
    def __create_game_config_with_no_enemy_spawning(self):
        cfg_file = tempfile.NamedTemporaryFile(mode="w", delete=False)
        cfg_file.write(
            "raise_your_sword:\n"
            "  configuration: {}\n"
        )
        cfg_file.close()

        return GameConfig(
            GraphicsConfig(
                display_size=(260, 190),
                scaling_factor=3
            ),
            AiConfig(
                idle_time=Range(500, 500),
                walk_time=Range(100, 100),
                attack_initiation_distance=25
            ),
            SpawningConfig(
                cfg_file=cfg_file.name,
                time_between_spawning_one=Range(100, 100),
                time_between_spawning_a_group=Range(4000, 4000),
                number_of_enemies_to_spawn_at_once=10,
                total_number_of_enemies_to_spawn=0,
            )
        )

    def test_game_update_method_called_once_per_game_loop_iteration(self):
        game = StubGame()

        game_loop = GameLoop(
            game,
            StubRenderer(),
            StubEventQueue([[], [StubEvent(pygame.QUIT)]]),
            StubClock()
        )

        game_loop.start()

        self.assertEqual(game.update_called_count, 1)

    def test_game_can_be_won_by_defeating_the_last_enemy(self):
        config = self.__create_game_config_with_no_enemy_spawning()

        game = Game(config=config, skip_intro=True)

        game.add_enemy(create_enemy(
            starting_position=(
                (config.graphics.display_width - 48) // 2,
                (config.graphics.display_height - 48) // 2 - 7 + 35
            ),
            animation = load_animation(
                os.path.join(dirname, "..", "assets", "character_skeleton_animations.yaml")
            ),
            ai_config=config.ai
        ))

        game_loop = GameLoop(
            game,
            StubRenderer(),
            StubEventQueue(
                [[StubEvent(pygame.KEYDOWN, pygame.K_x)]] + (10 * 60) * [[]] +
                    [[StubEvent(pygame.QUIT)]]
            ),
            StubClock()
        )

        game_loop.start()

        self.assertTrue(game.finished)
        self.assertEqual(game.state, "VictoryScreenState")

    def test_game_can_be_lost_by_getting_hit_by_an_enemy(self):
        config = self.__create_game_config_with_no_enemy_spawning()

        game = Game(config=config, skip_intro=True)

        game.add_enemy(create_enemy(
            starting_position=(
                (config.graphics.display_width - 48) // 2,
                (config.graphics.display_height - 48) // 2 - 7 - 48
            ),
            animation = load_animation(
                os.path.join(dirname, "..", "assets", "character_skeleton_animations.yaml")
            ),
            ai_config=config.ai
        ))

        game_loop = GameLoop(
            game,
            StubRenderer(),
            StubEventQueue((10 * 60) * [[]] + [[StubEvent(pygame.QUIT)]]),
            StubClock()
        )

        game_loop.start()

        self.assertTrue(game.finished)
        self.assertEqual(game.state, "DefeatScreenState")
