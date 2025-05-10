from configuration.utils import load_config

class SpawningConfig:
    def __init__(self, *, cfg_file, time_between_spawning_one, time_between_spawning_a_group,
            number_of_enemies_to_spawn_at_once, total_number_of_enemies_to_spawn):
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
        return self.__time_between_spawning_one

    @property
    def time_between_spawning_a_group(self):
        return self.__time_between_spawning_a_group

    @property
    def number_of_enemies_to_spawn_at_once(self):
        return self.__number_of_enemies_to_spawn_at_once

    @property
    def total_number_of_enemies_to_spawn(self):
        return self.__total_number_of_enemies_to_spawn
