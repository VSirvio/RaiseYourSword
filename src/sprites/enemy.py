import pygame

from direction import DOWN, UP, LEFT, RIGHT

BOUNDING_BOX = pygame.Rect((20, 22), (8, 11))

WEAPON_HITBOX = {
    DOWN: pygame.Rect((0, 26), (48, 22)),
    UP: pygame.Rect((0, 0), (48, 22)),
    LEFT: pygame.Rect((0, 0), (22, 48)),
    RIGHT: pygame.Rect((26, 0), (22, 48))
}

class Enemy(pygame.sprite.Sprite):
    def __init__(self, animations):
        super().__init__()

        self.__facing_direction = DOWN
        self.__state = "idle"

        self.__animations = animations

        self.__index = 0

        self.image = self.__animations[self.__state][self.__facing_direction][self.__index]

        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 27

        self.__timer = 0

    def update(self, dt, **kwargs):
        player = kwargs["player"]

        self.__timer += dt

        frametime = 1000 / self.__animations[self.__state]["framerate"]
        while self.__timer >= frametime:
            num_of_frames = len(self.__animations[self.__state][self.__facing_direction])
            self.__index = (self.__index + 1) % num_of_frames
            self.__timer -= frametime

            if self.__index == 0:
                if self.__state == "attack":
                    self.__state = "idle"
                elif self.__state == "idle" and not player.has_been_defeated:
                    self.__state = "attack"

            weapon_hitbox_relative_to_screen = pygame.Rect(
                self.rect.x + WEAPON_HITBOX[self.__facing_direction].x,
                self.rect.y + WEAPON_HITBOX[self.__facing_direction].y,
                WEAPON_HITBOX[self.__facing_direction].width,
                WEAPON_HITBOX[self.__facing_direction].height
            )
            if (self.__state == "attack" and self.__index == num_of_frames - 1
                    and weapon_hitbox_relative_to_screen.colliderect(player.bounding_box)):
                player.lose()

        self.image = self.__animations[self.__state][self.__facing_direction][self.__index]

    @property
    def bounding_box(self):
        return pygame.Rect(
            self.rect.x + BOUNDING_BOX.x,
            self.rect.y + BOUNDING_BOX.y,
            BOUNDING_BOX.width,
            BOUNDING_BOX.height
        )
