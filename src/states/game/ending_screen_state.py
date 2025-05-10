import pygame

class EndingScreenState:
    def __init__(self, message_image, message_position, instructions_image, instructions_position):
        self.__message_image = message_image
        self.__message_position = message_position
        self.__instructions_image = instructions_image
        self.__instructions_position = instructions_position

        self.__bg_sprite = None
        self.__message_sprite = None
        self.__instr_sprite = None
        self.__sprite_group = None

    def enter(self, game):
        display_width = game.config.graphics.display_width
        display_height = game.config.graphics.display_height

        self.__bg_sprite = pygame.sprite.Sprite()
        self.__bg_sprite.image = pygame.Surface((display_width, display_height), pygame.SRCALPHA)
        self.__bg_sprite.image.fill(pygame.Color(0, 0, 0, 190))
        self.__bg_sprite.rect = self.__bg_sprite.image.get_rect()

        self.__message_sprite = pygame.sprite.Sprite()
        self.__message_sprite.image = self.__message_image
        self.__message_sprite.rect = self.__message_sprite.image.get_rect()
        self.__message_sprite.rect.x, self.__message_sprite.rect.y = self.__message_position

        self.__instr_sprite = pygame.sprite.Sprite()
        self.__instr_sprite.image = self.__instructions_image
        self.__instr_sprite.rect = self.__instr_sprite.image.get_rect()
        self.__instr_sprite.rect.x, self.__instr_sprite.rect.y = self.__instructions_position

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
