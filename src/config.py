import os

from configuration.ai_config import AiConfig
from configuration.game_config import GameConfig
from configuration.graphics_config import GraphicsConfig
from configuration.spawning_config import SpawningConfig
from utils import Range

dirname = os.path.dirname(__file__)

def generate_configuration():
    return GameConfig(
        GraphicsConfig(
            display_size=(260, 190),
            scaling_factor=3
        ),
        AiConfig(
            idle_time=Range(500, 2000),
            walk_time=Range(100, 500),
            attack_initiation_distance=25
        ),
        SpawningConfig(
            cfg_file=os.path.join(dirname, "config.yaml"),
            time_between_spawning_one=Range(100, 200),
            time_between_spawning_a_group=Range(4000, 5000),
            number_of_enemies_to_spawn_at_once=10,
            total_number_of_enemies_to_spawn=30,
        )
    )
