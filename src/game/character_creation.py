import os

import pygame

from components.animations_component import AnimationsComponent
from components.physics_component import PhysicsComponent
from components.player_physics import PlayerPhysics
from direction.character_direction import CharacterDirection
from direction.direction import NONE, DOWN, UP, LEFT, RIGHT
from direction.player_direction import PlayerDirection
import states.ai.idle_state
import states.player.idle_state
from .character import Character
from .config import DISPLAY_HEIGHT, DISPLAY_WIDTH, ENEMY_WALKING_SPEED

dirname = os.path.dirname(__file__)

def create_enemy(starting_position, animation):
    return Character(
        initial_state=states.ai.idle_state.IdleState(),
        starting_position=starting_position,
        direction=CharacterDirection(facing=DOWN, moving=NONE),
        animations=AnimationsComponent(animation),
        physics=PhysicsComponent(
            walking_speed=ENEMY_WALKING_SPEED,
            bounding_box=pygame.Rect((16, 20), (16, 20)),
            character_hitbox=pygame.Rect((14, 10), (20, 33)),
            weapon_hitbox={
                DOWN: pygame.Rect((7, 26), (25, 17)),
                UP: pygame.Rect((16, 5), (25, 16)),
                LEFT: pygame.Rect((6, 16), (14, 25)),
                RIGHT: pygame.Rect((29, 14), (14, 27))
            }
        )
    )

def create_player(animation, game_area_bounds):
    return Character(
        initial_state=states.player.idle_state.IdleState(),
        starting_position=(
            (DISPLAY_WIDTH - 48) // 2,
            (DISPLAY_HEIGHT - 48) // 2 - 7
        ),
        direction=PlayerDirection(facing=DOWN, moving=NONE, controlled_toward=NONE),
        animations=AnimationsComponent(animation),
        physics=PlayerPhysics(
            walking_speed=75,
            bounding_box=pygame.Rect((16, 14), (16, 25)),
            character_hitbox=pygame.Rect((17, 7), (14, 32)),
            weapon_hitbox={
                DOWN: pygame.Rect((0, 24), (41, 24)),
                UP: pygame.Rect((7, 0), (41, 24)),
                LEFT: pygame.Rect((0, 7), (24, 41)),
                RIGHT: pygame.Rect((24, 6), (24, 42))
            },
            game_area_bounds=game_area_bounds
        )
    )
