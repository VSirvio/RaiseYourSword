import os
import sys

import yaml

dirname = os.path.dirname(__file__)

CONFIG_FILE = "config.yaml"

config = {}

try:
    with open(os.path.join(dirname, "..", CONFIG_FILE), "r", encoding="UTF-8") as file:
        yaml_data = yaml.safe_load(file)
except OSError:
    sys.exit(f"ERROR: Failed to read the file \"{CONFIG_FILE}\"")
else:
    if "raise_your_sword" not in yaml_data:
        sys.exit(f"ERROR: \"{CONFIG_FILE}\" requires \"raise_your_sword\" key at the root level")

    if "configuration" not in yaml_data["raise_your_sword"]:
        sys.exit(f"ERROR: \"{CONFIG_FILE}\" requires \"configuration\" key "
            "under the \"raise_your_sword\" key")

    config = yaml_data["raise_your_sword"]["configuration"]

    if "total_number_of_enemies_to_spawn" in config:
        if type(config["total_number_of_enemies_to_spawn"]) not in (float, int):
            sys.exit(f"ERROR: The key \"total_number_of_enemies_to_spawn\" in \"{CONFIG_FILE}\" "
                "should have a numeric value")

        if config["total_number_of_enemies_to_spawn"] < 1:
            sys.exit("ERROR: The value of the key \"total_number_of_enemies_to_spawn\" "
                f"in \"{CONFIG_FILE}\" should be at least 1")


DISPLAY_WIDTH = 260
DISPLAY_HEIGHT = 190

GRAPHICS_SCALING_FACTOR = 3

ENEMY_WALKING_SPEED = 50
ENEMY_ATTACK_INITIATION_DISTANCE = 25
ENEMY_AI_IDLE_TIME_MIN = 500
ENEMY_AI_IDLE_TIME_MAX = 2000
ENEMY_AI_WALK_TIME_MIN = 100
ENEMY_AI_WALK_TIME_MAX = 500
ENEMY_MIN_TIME_BETWEEN_SPAWNING_A_GROUP = 4000
ENEMY_MAX_TIME_BETWEEN_SPAWNING_A_GROUP = 5000
ENEMY_MIN_TIME_BETWEEN_SPAWNING_ONE = 100
ENEMY_MAX_TIME_BETWEEN_SPAWNING_ONE = 200
NUMBER_OF_ENEMIES_TO_SPAWN_AT_ONCE = 10
TOTAL_NUMBER_OF_ENEMIES_TO_SPAWN = config.get("total_number_of_enemies_to_spawn", 30)
MAX_NUM_OF_DEAD_ENEMIES_ON_THE_SCREEN = 50
