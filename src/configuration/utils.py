import sys

import yaml

def load_config(cfg_file_path):
    try:
        with open(cfg_file_path, "r", encoding="UTF-8") as file:
            yaml_data = yaml.safe_load(file)
    except OSError:
        sys.exit(f"ERROR: Failed to read the file \"{cfg_file_path}\"")

    if "raise_your_sword" not in yaml_data:
        sys.exit(f"ERROR: \"{cfg_file_path}\" requires \"raise_your_sword\" key at the root level")

    if "configuration" not in yaml_data["raise_your_sword"]:
        sys.exit(f"ERROR: \"{cfg_file_path}\" requires \"configuration\" key "
            "under the \"raise_your_sword\" key")

    config_data = yaml_data["raise_your_sword"]["configuration"]
    config = {}

    if "total_number_of_enemies_to_spawn" in config_data:
        total_number_of_enemies_to_spawn = config_data["total_number_of_enemies_to_spawn"]

        if type(total_number_of_enemies_to_spawn) not in (float, int):
            sys.exit("ERROR: The key \"total_number_of_enemies_to_spawn\" "
                f"in \"{cfg_file_path}\" should have a numeric value")

        if total_number_of_enemies_to_spawn < 1:
            sys.exit("ERROR: The value of the key \"total_number_of_enemies_to_spawn\" "
                f"in \"{cfg_file_path}\" should be at least 1")

        config["total_number_of_enemies_to_spawn"] = total_number_of_enemies_to_spawn

    return config
