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

dirname = os.path.dirname(__file__)

def create_enemy(starting_position, animation, ai_config):
    """Creates a Character instance configured as enemy character.

    Args:
        starting_position: (X,Y) tuple with the initial position for the enemy.
        animation: The CharacterAnimation instance containing enemy animations.
        ai_config: The AiConfig instance of the game.

    Returns:
        A Character instance that has been set up as enemy character.
    """

    return Character(
        initial_state=states.ai.idle_state.IdleState(),
        starting_position=starting_position,
        direction=CharacterDirection(facing=DOWN, moving=NONE),
        animations=AnimationsComponent(animation),
        physics=PhysicsComponent(
            walking_speed=50,
            bounding_box=pygame.Rect((16, 20), (16, 20)),
            character_hitbox=pygame.Rect((14, 10), (20, 33)),
            weapon_hitbox={
                DOWN: pygame.Rect((7, 26), (25, 17)),
                UP: pygame.Rect((16, 5), (25, 16)),
                LEFT: pygame.Rect((6, 16), (14, 25)),
                RIGHT: pygame.Rect((29, 14), (14, 27))
            }
        ),
        config=ai_config
    )

def create_player(starting_position, animation, game_area_bounds):
    """Creates a Character instance configured as player character.

    Args:
        starting_position: (X,Y) tuple with the initial position for the player.
        animation: The CharacterAnimation instance containing player animations.
        game_area_bounds: Pygame Rect of the screen area that player can't exit.

    Returns:
        A Character instance that has been set up as player character.
    """

    return Character(
        initial_state=states.player.idle_state.IdleState(),
        starting_position=starting_position,
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
