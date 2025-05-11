import tempfile
import unittest

from configuration.ai_config import AiConfig
from configuration.game_config import GameConfig
from configuration.graphics_config import GraphicsConfig
from configuration.spawning_config import SpawningConfig
from game.enemy_spawner import EnemySpawner
from utils import Range


class StubGame:
    def __init__(self, config):
        self.config = config
        self.add_enemy_count = 0

    def add_enemy(self, new_enemy):
        self.add_enemy_count += 1

    def another_character_overlaps_with(self, character):
        return False


class TestEnemySpawner(unittest.TestCase):
    def setUp(self):
        cfg_file = tempfile.NamedTemporaryFile(mode="w", delete=False)
        cfg_file.write(
            "raise_your_sword:\n"
            "  configuration: {}\n"
        )
        cfg_file.close()

        self.time_between_spawning_one = 100
        self.time_between_spawning_a_group = 4000
        self.number_of_enemies_to_spawn_at_once = 10

        self.config = GameConfig(
            GraphicsConfig(
                display_size=(260, 190),
                scaling_factor=3
            ),
            AiConfig(
                idle_time=Range(1000000, 1000000),
                walk_time=Range(100, 100),
                attack_initiation_distance=25
            ),
            SpawningConfig(
                cfg_file=cfg_file.name,
                time_between_spawning_one=Range(
                    self.time_between_spawning_one,
                    self.time_between_spawning_one
                ),
                time_between_spawning_a_group=Range(
                    self.time_between_spawning_a_group,
                    self.time_between_spawning_a_group
                ),
                number_of_enemies_to_spawn_at_once=self.number_of_enemies_to_spawn_at_once,
                total_number_of_enemies_to_spawn=30,
            )
        )

    def test_spawns_enemies(self):
        game = StubGame(self.config)
        spawner = EnemySpawner(game)

        spawner.spawn_enemies(
            dt=self.number_of_enemies_to_spawn_at_once*self.time_between_spawning_one+1,
            game=game
        )

        self.assertGreater(game.add_enemy_count, 0)

    def test_spawns_correct_number_of_enemies_in_a_group(self):
        game = StubGame(self.config)
        spawner = EnemySpawner(game)

        spawner.spawn_enemies(
            dt=self.time_between_spawning_a_group-1,
            game=game
        )

        self.assertEqual(game.add_enemy_count, self.number_of_enemies_to_spawn_at_once)

    def test_spawns_next_group_after_correct_duration(self):
        game = StubGame(self.config)
        spawner = EnemySpawner(game)

        spawner.spawn_enemies(
            dt=self.time_between_spawning_a_group+1,
            game=game
        )

        self.assertGreater(game.add_enemy_count, self.number_of_enemies_to_spawn_at_once)
