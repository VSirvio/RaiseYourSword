import sys

import yaml

def load_config(cfg_file_path):
    """Creates a configuration dict based on the given YAML file.

    Args:
        cfg_file_path: The path to the game configuration YAML file as a string.

    Returns:
        A dict containing the game configuration that was loaded from the file.
    """

    try:
        with open(cfg_file_path, "r", encoding="UTF-8") as file:
            yaml_data = yaml.safe_load(file)
    except OSError:
        sys.exit(f"ERROR: Failed to read the file \"{cfg_file_path}\"")

    if not isinstance(yaml_data, dict) or "raise_your_sword" not in yaml_data:
        sys.exit(f"ERROR: \"{cfg_file_path}\" requires \"raise_your_sword\" key at the root level")

    if (not isinstance(yaml_data["raise_your_sword"], dict) or
            "configuration" not in yaml_data["raise_your_sword"]):
        sys.exit(f"ERROR: \"{cfg_file_path}\" requires \"configuration\" key "
            "under the \"raise_your_sword\" key")

    config_data = yaml_data["raise_your_sword"]["configuration"]
    config = {}

    if isinstance(config_data, dict) and "total_number_of_enemies_to_spawn" in config_data:
        total_number_of_enemies_to_spawn = config_data["total_number_of_enemies_to_spawn"]

        if type(total_number_of_enemies_to_spawn) not in (float, int):
            sys.exit("ERROR: The key \"total_number_of_enemies_to_spawn\" "
                f"in \"{cfg_file_path}\" should have a numeric value")

        if total_number_of_enemies_to_spawn < 1:
            sys.exit("ERROR: The value of the key \"total_number_of_enemies_to_spawn\" "
                f"in \"{cfg_file_path}\" should be at least 1")

        config["total_number_of_enemies_to_spawn"] = total_number_of_enemies_to_spawn

    return config
