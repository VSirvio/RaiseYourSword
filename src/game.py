import pygame
from pygame import Color

from config import DISPLAY_WIDTH, DISPLAY_HEIGHT
from direction import DOWN, UP, LEFT, RIGHT
from sprites.background import Background
from sprites.enemy import Enemy
from sprites.player import Player
from utils import load_animation

class Game:
    def __init__(self):
        self.__background = Background()
        self.__player = Player({
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
                DOWN: load_animation("warrior", 8, 6),
                UP: load_animation("warrior", 9, 6),
                LEFT: load_animation("warrior", 10, 6),
                RIGHT: load_animation("warrior", 11, 6)
            }
        })
        self.__enemy = Enemy({
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
                DOWN: load_animation("skeleton", 8, 8),
                UP: load_animation("skeleton", 9, 8),
                LEFT: load_animation("skeleton", 10, 8),
                RIGHT: load_animation("skeleton", 11, 8)
            }
        })

        self.__characters = pygame.sprite.Group(self.__player, self.__enemy)

        self.__all_sprites = pygame.sprite.LayeredUpdates(self.__background, self.__characters)

        # Move background to layer -1000 to make sure that it is behind all other sprites
        self.__all_sprites.change_layer(self.__background, -1000)

        self.__finished = False

        transparent_black = Color(0, 0, 0, 190)
        result_screen_font = pygame.font.SysFont(name="Sans", size=17, bold=True)

        self.__victory_screen = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA)
        self.__victory_screen.fill(transparent_black)
        victory_screen_text = result_screen_font.render("YOU HAVE WON", True, Color("white"))
        self.__victory_screen.blit(victory_screen_text, (60, 90))

        self.__game_over_screen = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA)
        self.__game_over_screen.fill(transparent_black)
        game_over_screen_text = result_screen_font.render("GAME OVER", True, Color("white"))
        self.__game_over_screen.blit(game_over_screen_text, (80, 90))

    def draw(self, surface):
        # Set each character sprite's layer value to be the same as its Y position so that the
        # sprites further away (the sprites that have a lower Y value) are shown behind the sprites
        # closer (i.e. the sprites further away have a lower layer value than the sprites closer)
        for sprite in self.__characters:
            self.__all_sprites.change_layer(sprite, sprite.rect.y)

        self.__all_sprites.draw(surface)

        if self.__finished:
            if self.__player.has_been_defeated:
                surface.blit(self.__game_over_screen, (0, 0))
            else:
                surface.blit(self.__victory_screen, (0, 0))

    def update(self, dt):
        self.__all_sprites.update(dt, player=self.__player, enemy=self.__enemy)

        if not self.__finished and (self.__player.hit_an_enemy or self.__enemy.hit_the_player):
            if self.__player.hit_an_enemy:
                self.__characters.remove(self.__enemy)
                self.__all_sprites.remove(self.__enemy)
            else:
                self.__player.lose()
            self.__finished = True

    def handle_input(self, event, direction_pressed):
        self.__player.handle_input(event, direction_pressed, self.__enemy)

    @property
    def finished(self):
        return self.__finished
