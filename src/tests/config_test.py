import tempfile
import unittest

from configuration.utils import load_config

class TestConfig(unittest.TestCase):
    def __create_cfg_file(self, content):
        cfg_file = tempfile.NamedTemporaryFile(mode="w", delete=False)
        cfg_file.write(content)
        cfg_file.close()
        return cfg_file.name

    def test_setting_total_number_of_enemies(self):
        cfg_data = (
            "raise_your_sword:\n"
            "  configuration:\n"
            "    total_number_of_enemies_to_spawn: 458\n"
        )

        cfg_file = self.__create_cfg_file(cfg_data)

        self.assertEqual(load_config(cfg_file), {"total_number_of_enemies_to_spawn": 458})

    def test_missing_cfg_file(self):
        with self.assertRaises(SystemExit):
            load_config("missing_cfg_file.yaml")

    def test_empty_cfg_file(self):
        with self.assertRaises(SystemExit):
            load_config(self.__create_cfg_file(""))

    def test_incorrect_structure(self):
        cfg_data = (
            "raise_your_sword:\n"
            "  total_number_of_enemies_to_spawn: 71\n"
        )

        with self.assertRaises(SystemExit):
            load_config(self.__create_cfg_file(cfg_data))
