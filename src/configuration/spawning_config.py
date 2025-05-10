from configuration.utils import load_config

class SpawningConfig:
    """Stores the enemy spawning configuration for the game."""

    def __init__(self, *, cfg_file, time_between_spawning_one, time_between_spawning_a_group,
            number_of_enemies_to_spawn_at_once, total_number_of_enemies_to_spawn):
        """Creates an enemy spawning configuration with the given parameters.

        Args:
            cfg_file: The path to the game configuration YAML file as a string.
            time_between_spawning_one: A Range of milliseconds.
            time_between_spawning_a_group: A Range of milliseconds.
            number_of_enemies_to_spawn_at_once: An integer value.
            total_number_of_enemies_to_spawn: An integer value.
        """

        config_from_file = load_config(cfg_file)

        self.__time_between_spawning_one = time_between_spawning_one
        self.__time_between_spawning_a_group = time_between_spawning_a_group
        self.__number_of_enemies_to_spawn_at_once = number_of_enemies_to_spawn_at_once
        self.__total_number_of_enemies_to_spawn = config_from_file.get(
            "total_number_of_enemies_to_spawn",
            total_number_of_enemies_to_spawn
        )

    @property
    def time_between_spawning_one(self):
        """The time between spawning the enemies of a group in milliseconds."""

        return self.__time_between_spawning_one

    @property
    def time_between_spawning_a_group(self):
        """The time between spawning enemy groups in milliseconds."""

        return self.__time_between_spawning_a_group

    @property
    def number_of_enemies_to_spawn_at_once(self):
        """The number of enemies in one spawn group."""

        return self.__number_of_enemies_to_spawn_at_once

    @property
    def total_number_of_enemies_to_spawn(self):
        """The total number of enemies to spawn in a game."""

        return self.__total_number_of_enemies_to_spawn
