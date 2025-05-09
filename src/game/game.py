import os

import pygame

from animation.utils import load_animation
import states.game.cinematic_texts_state
import states.game.play_state
import states.player.idle_state
from . import events
from .background import Background
from .character_creation import create_player
from .config import (
    DISPLAY_HEIGHT,
    DISPLAY_WIDTH,
    MAX_NUM_OF_DEAD_ENEMIES_ON_THE_SCREEN,
    TOTAL_NUMBER_OF_ENEMIES_TO_SPAWN
)

dirname = os.path.dirname(__file__)

class Game:
    """Responsible for the game's graphics and logic."""

    def __init__(self, skip_intro):
        if skip_intro:
            self.__state = states.game.play_state.PlayState()
        else:
            image_files = [f"cinematic_text_{i}.png" for i in range(1, 5)]
            self.__state = states.game.cinematic_texts_state.CinematicTextsState(
                [os.path.join(dirname, "..", "assets", file) for file in image_files]
            )

        self.__background = Background()
        game_area_bounds = pygame.Rect(-5, -13, DISPLAY_WIDTH + 5 + 6, DISPLAY_HEIGHT + 13 + 17)
        self.__player = create_player(
            load_animation(
                os.path.join(dirname, "..", "assets", "character_warrior_animations.yaml")
            ),
            game_area_bounds
        )
        self.__enemies = []

        self.__characters = pygame.sprite.Group(self.__player.sprite)

        self.__all_sprites = pygame.sprite.LayeredUpdates(self.__background, self.__characters)

        # Move background to layer -1000 to make sure that it is behind all other sprites
        self.__all_sprites.change_layer(self.__background, -1000)

        self.__enemies_spawned_but_not_yet_removed = 0
        self.__enemies_to_still_spawn = TOTAL_NUMBER_OF_ENEMIES_TO_SPAWN

    def __all_enemies_have_been_defeated(self):
        if len(self.__enemies) > self.__enemies_spawned_but_not_yet_removed:
            self.__enemies_to_still_spawn -= (len(self.__enemies) -
                self.__enemies_spawned_but_not_yet_removed)
            self.__enemies_spawned_but_not_yet_removed = len(self.__enemies)

        return (self.__enemies_to_still_spawn <= 0 and
            all(enemy.state == "dead" for enemy in self.__enemies))

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

        self.__enemies.sort(key=lambda enemy: enemy.state != "dead")
        dead_enemies = sum(1 if enemy.state == "dead" else 0 for enemy in self.__enemies)
        while dead_enemies > MAX_NUM_OF_DEAD_ENEMIES_ON_THE_SCREEN:
            removed_enemy = self.__enemies.pop(0)
            self.__characters.remove(removed_enemy.sprite)
            self.__all_sprites.remove(removed_enemy.sprite)
            dead_enemies -= 1
            self.__enemies_spawned_but_not_yet_removed -= 1

        self.__player.update(dt, opponents=self.__enemies, other_characters=[])
        for enemy in self.__enemies:
            other_enemies = [e for e in self.__enemies if e != enemy]
            enemy.update(dt, opponents=[self.__player], other_characters=other_enemies)

        self.__state.update(dt, self)

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
