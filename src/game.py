import pygame

from config import DISPLAY_WIDTH, DISPLAY_HEIGHT
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
                "down": load_animation("warrior", 0, 5),
                "up": load_animation("warrior", 1, 5),
                "left": load_animation("warrior", 2, 5),
                "right": load_animation("warrior", 3, 5)
            },
            "walk": {
                "framerate": 12,
                "down": load_animation("warrior", 4, 8),
                "up": load_animation("warrior", 5, 8),
                "left": load_animation("warrior", 6, 8),
                "right": load_animation("warrior", 7, 8)
            },
            "attack": {
                "framerate": 15,
                "down": load_animation("warrior", 8, 6),
                "up": load_animation("warrior", 9, 6),
                "left": load_animation("warrior", 10, 6),
                "right": load_animation("warrior", 11, 6)
            }
        })
        self.__enemy = Enemy({
            "idle": {
                "framerate": 4,
                "down": load_animation("skeleton", 0, 6),
                "up": load_animation("skeleton", 1, 6),
                "left": load_animation("skeleton", 2, 6),
                "right": load_animation("skeleton", 3, 6)
            },
            "walk": {
                "framerate": 12,
                "down": load_animation("skeleton", 4, 6),
                "up": load_animation("skeleton", 5, 6),
                "left": load_animation("skeleton", 6, 6),
                "right": load_animation("skeleton", 7, 6)
            },
            "attack": {
                "framerate": 15,
                "down": load_animation("skeleton", 8, 8),
                "up": load_animation("skeleton", 9, 8),
                "left": load_animation("skeleton", 10, 8),
                "right": load_animation("skeleton", 11, 8)
            }
        })

        self.__characters = pygame.sprite.Group(self.__player, self.__enemy)

        self.__all_sprites = pygame.sprite.LayeredUpdates(self.__background, self.__characters)

        # Move background to layer -1000 to make sure that it is behind all other sprites
        self.__all_sprites.change_layer(self.__background, -1000)

        self.__finished = False

        self.__victory_screen = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA)
        self.__victory_screen.fill(pygame.Color(0, 0, 0, 190))
        font = pygame.font.SysFont(name="Sans", size=50, bold=True)
        self.__victory_screen.blit(font.render("YOU HAVE WON", True, pygame.Color(255, 255, 255)), (210, 270))

    def draw(self, surface):
        # Set each character sprite's layer value to be the same as its Y position so that the
        # sprites further away (the sprites that have a lower Y value) are shown behind the sprites
        # closer (i.e. the sprites further away have a lower layer value than the sprites closer)
        for sprite in self.__characters:
            self.__all_sprites.change_layer(sprite, sprite.rect.y)

        self.__all_sprites.draw(surface)

        if self.__finished:
            surface.blit(self.__victory_screen, (0, 0))

    def update(self, dt):
        self.__all_sprites.update(dt, self.__enemy)

    def walk(self, vert_direction, horiz_direction):
        self.__player.walk(vert_direction, horiz_direction)

    def attack(self):
        enemy_was_hit = self.__player.attack(self.__enemy)
        if enemy_was_hit:
            self.__characters.remove(self.__enemy)
            self.__all_sprites.remove(self.__enemy)
            self.__finished = True

    @property
    def finished(self):
        return self.__finished
