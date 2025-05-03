from random import randint

import pygame
from pygame import Color

import ai.idle_state
from character import Character
from character_direction import CharacterDirection
from components.animations_component import AnimationsComponent
from components.physics_component import PhysicsComponent
from components.player_physics import PlayerPhysics
from config import (
    DISPLAY_WIDTH,
    DISPLAY_HEIGHT,
    ENEMY_WALKING_SPEED,
    ENEMY_MIN_TIME_BETWEEN_SPAWNING,
    ENEMY_MAX_TIME_BETWEEN_SPAWNING,
    NUMBER_OF_ENEMIES_TO_SPAWN
)
from direction import NONE, DOWN, UP, LEFT, RIGHT
import events
from player_direction import PlayerDirection
from sprites.background import Background
import states.idle_state
from utils import load_animation

class Game:
    """Responsible for the game's graphics and logic."""

    def __init__(self):
        self.__background = Background()
        self.__player = Character(
            role="player",
            initial_state=states.idle_state.IdleState(),
            starting_position=(
                (DISPLAY_WIDTH - 48) // 2,
                (DISPLAY_HEIGHT - 48) // 2 - 7
            ),
            direction=PlayerDirection(facing=DOWN, moving=NONE, controlled_toward=NONE),
            animations=AnimationsComponent({
                "idle": {
                    "framerate": 4,
                    DOWN: load_animation("warrior", 0, 5),
                    UP: load_animation("warrior", 1, 5),
                    LEFT: load_animation("warrior", 2, 5),
                    RIGHT: load_animation("warrior", 3, 5)
                },
                "walk": {
                    "framerate": 12,
                    DOWN: load_animation("warrior", 4, 8),
                    UP: load_animation("warrior", 5, 8),
                    LEFT: load_animation("warrior", 6, 8),
                    RIGHT: load_animation("warrior", 7, 8)
                },
                "attack": {
                    "framerate": 15,
                    "damage_frames": [2, 3],
                    DOWN: load_animation("warrior", 8, 6),
                    UP: load_animation("warrior", 9, 6),
                    LEFT: load_animation("warrior", 10, 6),
                    RIGHT: load_animation("warrior", 11, 6)
                },
                "dying": {
                    "framerate": 12,
                    DOWN: load_animation("warrior", 12, 5),
                    UP: load_animation("warrior", 13, 6),
                    LEFT: load_animation("warrior", 14, 5),
                    RIGHT: load_animation("warrior", 15, 5)
                },
                "dead": {
                    "framerate": 1,
                    DOWN: load_animation("warrior", 12, 1, 4),
                    UP: load_animation("warrior", 13, 1, 5),
                    LEFT: load_animation("warrior", 14, 1, 4),
                    RIGHT: load_animation("warrior", 15, 1, 4)
                }
            }),
            physics=PlayerPhysics(
                walking_speed=75,
                bounding_box=pygame.Rect((11, 6), (25, 36)),
                weapon_hitbox={
                    DOWN: pygame.Rect((0, 24), (48, 24)),
                    UP: pygame.Rect((0, 0), (48, 24)),
                    LEFT: pygame.Rect((0, 0), (24, 48)),
                    RIGHT: pygame.Rect((24, 0), (24, 48))
                },
                game_area_size=(DISPLAY_WIDTH, DISPLAY_HEIGHT)
            )
        )
        self.__enemies = []

        self.__characters = pygame.sprite.Group(self.__player.sprite)

        self.__all_sprites = pygame.sprite.LayeredUpdates(self.__background, self.__characters)

        # Move background to layer -1000 to make sure that it is behind all other sprites
        self.__all_sprites.change_layer(self.__background, -1000)

        self.__spawning_timer = 0
        self.__time_until_next_spawn = randint(
            ENEMY_MIN_TIME_BETWEEN_SPAWNING,
            ENEMY_MAX_TIME_BETWEEN_SPAWNING
        )
        self.__number_of_enemies_spawned_so_far = 0

        transparent_black = Color(0, 0, 0, 190)
        result_screen_font = pygame.font.SysFont(name="Sans", size=17, bold=True)

        self.__victory_screen = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA)
        self.__victory_screen.fill(transparent_black)
        victory_screen_text = result_screen_font.render("YOU HAVE WON", True, Color("white"))
        self.__victory_screen.blit(victory_screen_text, (61, 90))

        self.__game_over_screen = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA)
        self.__game_over_screen.fill(transparent_black)
        game_over_screen_text = result_screen_font.render("GAME OVER", True, Color("white"))
        self.__game_over_screen.blit(game_over_screen_text, (78, 90))

        restart_instructions_font = pygame.font.SysFont(name="Sans", size=10)
        restart_instructions_text = restart_instructions_font.render(
            "Press ENTER to restart or ESC to exit",
            False, # Antialiasing
            Color(150, 150, 150)
        )
        for screen in (self.__victory_screen, self.__game_over_screen):
            screen.blit(restart_instructions_text, (50, 175))

        sample_enemy = self.__create_enemy((0, 0))
        self.__enemy_width = sample_enemy.width
        self.__enemy_height = sample_enemy.height

    def __create_enemy(self, starting_position):
        return Character(
            role="enemy",
            initial_state=ai.idle_state.IdleState(),
            starting_position=starting_position,
            direction=CharacterDirection(facing=DOWN, moving=NONE),
            animations=AnimationsComponent({
                "idle": {
                    "framerate": 4,
                    DOWN: load_animation("skeleton", 0, 6),
                    UP: load_animation("skeleton", 1, 6),
                    LEFT: load_animation("skeleton", 2, 6),
                    RIGHT: load_animation("skeleton", 3, 6)
                },
                "walk": {
                    "framerate": 12,
                    DOWN: load_animation("skeleton", 4, 6),
                    UP: load_animation("skeleton", 5, 6),
                    LEFT: load_animation("skeleton", 6, 6),
                    RIGHT: load_animation("skeleton", 7, 6)
                },
                "attack": {
                    "framerate": 10,
                    "damage_frames": [6],
                    DOWN: load_animation("skeleton", 8, 8),
                    UP: load_animation("skeleton", 9, 8),
                    LEFT: load_animation("skeleton", 10, 8),
                    RIGHT: load_animation("skeleton", 11, 8)
                },
                "dying": {
                    "framerate": 12,
                    DOWN: load_animation("skeleton", 12, 8),
                    UP: load_animation("skeleton", 13, 8),
                    LEFT: load_animation("skeleton", 14, 8),
                    RIGHT: load_animation("skeleton", 15, 8)
                },
                "dead": {
                    "framerate": 1,
                    DOWN: load_animation("skeleton", 12, 1, 7),
                    UP: load_animation("skeleton", 13, 1, 7),
                    LEFT: load_animation("skeleton", 14, 1, 7),
                    RIGHT: load_animation("skeleton", 15, 1, 7)
                }
            }),
            physics=PhysicsComponent(
                walking_speed=ENEMY_WALKING_SPEED,
                bounding_box=pygame.Rect((20, 22), (8, 11)),
                weapon_hitbox={
                    DOWN: pygame.Rect((0, 26), (48, 22)),
                    UP: pygame.Rect((0, 0), (48, 22)),
                    LEFT: pygame.Rect((0, 0), (22, 48)),
                    RIGHT: pygame.Rect((26, 0), (22, 48))
                }
            )
        )

    def __all_enemies_have_been_defeated(self):
        return self.__enemies and all(enemy.state == "dead" for enemy in self.__enemies)

    def __last_enemy_is_dying(self):
        return (self.__enemies and not all(enemy.state == "dead" for enemy in self.__enemies) and
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

        if self.__player.state == "dead":
            surface.blit(self.__game_over_screen, (0, 0))
        elif self.__all_enemies_have_been_defeated():
            surface.blit(self.__victory_screen, (0, 0))

    def update(self, dt):
        """Updates the game logic.

        Args:
            dt: The time elapsed from the last call of this method.
        """

        self.__all_sprites.update(
            dt, opponents_to={"enemy": [self.__player], "player": self.__enemies}
        )

        self.__spawn_enemies(dt)

        if self.__last_enemy_is_dying():
            self.__player.handle_event(events.LastEnemyDying(), self.__enemies)

        if self.finished:
            self.__player.handle_event(events.GameEnded(), self.__enemies)

            for enemy in self.__enemies:
                enemy.handle_event(events.GameEnded(), self.__enemies)

    def handle(self, event):
        """Sends an event to the player object.

        Args:
            event: Event object of one of the classes from the "events" module.
        """

        self.__player.handle_event(event, self.__enemies)

    def __spawn_enemies(self, dt):
        if self.__number_of_enemies_spawned_so_far >= NUMBER_OF_ENEMIES_TO_SPAWN:
            return

        self.__spawning_timer += dt

        while (self.__spawning_timer >= self.__time_until_next_spawn and
                self.__number_of_enemies_spawned_so_far < NUMBER_OF_ENEMIES_TO_SPAWN):
            spawn_area_width = DISPLAY_WIDTH + self.__enemy_width
            spawn_area_height = DISPLAY_HEIGHT + self.__enemy_height

            random_number = randint(1, 2 * spawn_area_width + 2 * spawn_area_height)
            if random_number < spawn_area_width:
                spawning_position = (
                    -self.__enemy_width + random_number,
                    -self.__enemy_height
                )
            elif random_number < 2 * spawn_area_width:
                spawning_position = (
                    -self.__enemy_width + random_number - spawn_area_width,
                    DISPLAY_HEIGHT
                )
            elif random_number < 2 * spawn_area_width + spawn_area_height:
                spawning_position = (
                    -self.__enemy_width,
                    -self.__enemy_height + random_number - 2 * spawn_area_width
                )
            else:
                spawning_position = (
                    DISPLAY_WIDTH,
                    -self.__enemy_height + random_number - 2 * spawn_area_width - spawn_area_height
                )

            new_enemy = self.__create_enemy(spawning_position)
            self.__enemies.append(new_enemy)
            self.__characters.add(new_enemy.sprite)
            self.__all_sprites.add(new_enemy.sprite)

            self.__spawning_timer -= self.__time_until_next_spawn
            self.__time_until_next_spawn = randint(
                ENEMY_MIN_TIME_BETWEEN_SPAWNING,
                ENEMY_MAX_TIME_BETWEEN_SPAWNING
            )
            self.__number_of_enemies_spawned_so_far += 1

    @property
    def finished(self):
        """A boolean value indicating whether the game has finished."""

        return self.__all_enemies_have_been_defeated() or self.__player.state == "dead"
