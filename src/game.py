import os

import pygame

from character import Character
from components.animations_component import AnimationsComponent
from components.player_physics import PlayerPhysics
from config import DISPLAY_HEIGHT, DISPLAY_WIDTH, TOTAL_NUMBER_OF_ENEMIES_TO_SPAWN
from direction import NONE, DOWN, UP, LEFT, RIGHT
import events
from player_direction import PlayerDirection
from sprites.background import Background
import states.idle_state
import states.game.cinematic_texts_state
from utils import load_animation

dirname = os.path.dirname(__file__)

class Game:
    """Responsible for the game's graphics and logic."""

    def __init__(self):
        self.__state = states.game.cinematic_texts_state.CinematicTextsState([
            os.path.join(dirname, "assets", "cinematic_text_1.png"),
            os.path.join(dirname, "assets", "cinematic_text_2.png"),
            os.path.join(dirname, "assets", "cinematic_text_3.png"),
            os.path.join(dirname, "assets", "cinematic_text_4.png")
        ])

        self.__background = Background()
        game_area_bounds = pygame.Rect(-5, -13, DISPLAY_WIDTH + 5 + 6, DISPLAY_HEIGHT + 13 + 17)
        self.__player = Character(
            initial_state=states.idle_state.IdleState(),
            starting_position=(
                (DISPLAY_WIDTH - 48) // 2,
                (DISPLAY_HEIGHT - 48) // 2 - 7
            ),
            direction=PlayerDirection(facing=DOWN, moving=NONE, controlled_toward=NONE),
            animations=AnimationsComponent(
                load_animation("assets/character_warrior_animations.yaml")
            ),
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
        self.__enemies = []

        self.__characters = pygame.sprite.Group(self.__player.sprite)

        self.__all_sprites = pygame.sprite.LayeredUpdates(self.__background, self.__characters)

        # Move background to layer -1000 to make sure that it is behind all other sprites
        self.__all_sprites.change_layer(self.__background, -1000)

    def __all_enemies_have_been_defeated(self):
        return (len(self.__enemies) == TOTAL_NUMBER_OF_ENEMIES_TO_SPAWN and
            all(enemy.state == "dead" for enemy in self.__enemies))

    def __last_enemy_is_dying(self):
        return (len(self.__enemies) == TOTAL_NUMBER_OF_ENEMIES_TO_SPAWN and
            not all(enemy.state == "dead" for enemy in self.__enemies) and
            all(enemy.state in ("dead", "dying") for enemy in self.__enemies))

    def draw(self, surface):
        """Draws the current game screen on the given pygame surface.

        Args:
            surface: Pygame surface of the size DISPLAY_WIDTH x DISPLAY_HEIGHT.
        """

        # Set each character sprite's layer value to be the same as its Y position so that the
        # sprites further away (the sprites that have a lower Y value) are shown behind the sprites
        # closer (i.e. the sprites further away have a lower layer value than the sprites closer)
        for sprite in self.__characters:
            self.__all_sprites.change_layer(sprite, sprite.rect.y)

        self.__all_sprites.draw(surface)

        self.__state.draw(surface)

    def update(self, dt):
        """Updates the game logic.

        Args:
            dt: The time elapsed from the last call of this method.
        """

        self.__player.update(dt, opponents=self.__enemies, other_characters=[])
        for enemy in self.__enemies:
            other_enemies = list(filter(lambda x: x != enemy, self.__enemies))
            enemy.update(dt, opponents=[self.__player], other_characters=other_enemies)

        self.__state.update(dt, self)

        if self.__last_enemy_is_dying():
            self.__player.handle_event(events.LastEnemyDying(), self.__enemies)

        if self.finished:
            if self.__player.state == "dead":
                self.handle(events.PlayerLost())
            else:
                self.handle(events.PlayerWon())

            self.__player.handle_event(events.GameEnded(), self.__enemies)

            for enemy in self.__enemies:
                enemy.handle_event(events.GameEnded(), [self.__player])

    def handle(self, event):
        """Sends an event to the player object.

        Args:
            event: Event object of one of the classes from the "events" module.
        """

        new_state = self.__state.handle_event(event, self.__player, self.__enemies)
        if new_state is not None:
            self.__state = new_state

    def add_enemy(self, new_enemy):
        self.__enemies.append(new_enemy)
        self.__characters.add(new_enemy.sprite)
        self.__all_sprites.add(new_enemy.sprite)

    def another_character_overlaps_with(self, character):
        if character.bounding_box.colliderect(self.__player.bounding_box):
            return True

        for enemy in self.__enemies:
            if character.bounding_box.colliderect(enemy.bounding_box):
                return True

        return False

    @property
    def finished(self):
        """A boolean value indicating whether the game has finished."""

        return self.__all_enemies_have_been_defeated() or self.__player.state == "dead"
