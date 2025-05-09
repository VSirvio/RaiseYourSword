import os

import pygame
import yaml

from .animation import Animation
from .animation_set import AnimationSet
from .attack_animation import AttackAnimation
from .character_animation import CharacterAnimation

dirname = os.path.dirname(__file__)

def load_animation(animation_config_file):
    with open(os.path.join(dirname, animation_config_file), "r", encoding="UTF-8") as file:
        yaml_data = yaml.safe_load(file)

    frame_width = yaml_data["frame_size"]["width"]
    frame_height = yaml_data["frame_size"]["height"]

    sprite_sheet = pygame.image.load(
        os.path.join(dirname, os.path.dirname(animation_config_file), yaml_data["sprite_sheet"])
    )

    animation_sets = {}
    for set_name, set_data in yaml_data["animations"].items():
        animations_for_each_direction = {}
        for direction in ("down", "up", "left", "right"):
            frames = []
            for frame in set_data[direction]["frames"]:
                frames.append(
                    sprite_sheet.subsurface(
                        frame["x"] * frame_width,
                        frame["y"] * frame_height,
                        frame_width,
                        frame_height
                    )
                )

            if set_name == "attack":
                animations_for_each_direction[direction] = AttackAnimation(
                    framerate=set_data[direction]["framerate"],
                    damage_frames=set_data[direction]["damage_frames"],
                    frames=frames
                )
            else:
                animations_for_each_direction[direction] = Animation(
                    framerate=set_data[direction]["framerate"],
                    frames=frames
                )

        animation_sets[set_name] = AnimationSet(
            down=animations_for_each_direction["down"],
            up=animations_for_each_direction["up"],
            left=animations_for_each_direction["left"],
            right=animations_for_each_direction["right"],
        )

    return CharacterAnimation(
        sprite_sheet=sprite_sheet,
        frame_width=frame_width,
        frame_height=frame_height,
        animation_sets=animation_sets
    )
