import pygame

from game.config import DISPLAY_WIDTH, DISPLAY_HEIGHT

class EndingScreenState:
    def __init__(self, message_image, message_position, instructions_image, instructions_position):
        self.__bg_sprite = pygame.sprite.Sprite()
        self.__bg_sprite.image = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA)
        self.__bg_sprite.image.fill(pygame.Color(0, 0, 0, 190))
        self.__bg_sprite.rect = self.__bg_sprite.image.get_rect()

        self.__message_sprite = pygame.sprite.Sprite()
        self.__message_sprite.image = message_image
        self.__message_sprite.rect = self.__message_sprite.image.get_rect()
        self.__message_sprite.rect.x, self.__message_sprite.rect.y = message_position

        self.__instr_sprite = pygame.sprite.Sprite()
        self.__instr_sprite.image = instructions_image
        self.__instr_sprite.rect = self.__instr_sprite.image.get_rect()
        self.__instr_sprite.rect.x, self.__instr_sprite.rect.y = instructions_position

        self.__sprite_group = pygame.sprite.LayeredUpdates(
            self.__bg_sprite,
            self.__message_sprite,
            self.__instr_sprite
        )
        self.__sprite_group.change_layer(self.__bg_sprite, 1)
        self.__sprite_group.change_layer(self.__message_sprite, 2)
        self.__sprite_group.change_layer(self.__instr_sprite, 3)

    def update(self, *args):
        pass

    def handle_event(self, *args):
        pass

    @property
    def sprite_group(self):
        return self.__sprite_group
