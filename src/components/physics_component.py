from math import sqrt

from game import events

class PhysicsComponent:
    def __init__(self, walking_speed, bounding_box, character_hitbox, weapon_hitbox):
        self.__bounding_box = bounding_box
        self.__character_hitbox = character_hitbox
        self.__weapon_hitbox = weapon_hitbox

        self.__walk_timer = 0
        self.__walking_speed = walking_speed

    def update(self, dt, *args):
        owner = args[0]

        self.__walk_timer += dt

        dx, dy = owner.direction.moving.movement_vector

        time_per_px = 1000 / self.__walking_speed

        # When the walking direction is diagonal, we have to multiply the time
        # it takes to walk 1 pixel (time_per_px) by sqrt(2) = ~1.1,
        # because the distance moved on the screen per pixel is that much
        # longer (compare the diagonal length of a pixel to the width/height of
        # a pixel)
        if dx != 0 and dy != 0:
            time_per_px *= sqrt(2)

        while self.__walk_timer >= time_per_px:
            self.__walk_timer -= time_per_px
            self.__move(dx, dy, *args)

    def __move(self, dx, dy, *args):
        owner = args[0]
        opponents = args[1]
        other_characters = args[2]

        for character in other_characters:
            if character.state in ("dead", "dying"):
                continue

            dx, dy = owner.direction.moving.movement_vector
            if owner.bounding_box.move(dx, dy).colliderect(character.bounding_box):
                owner.handle_event(events.MovementObstructed(), opponents)
                return

        owner.x += dx
        owner.y += dy

    @property
    def bounding_box(self):
        return self.__bounding_box

    @property
    def character_hitbox(self):
        return self.__character_hitbox

    def does_attack_hit(self, attacker, target):
        weapon_hitbox = self.__weapon_hitbox[attacker.direction.facing]
        weapon_hitbox_relative_to_screen = weapon_hitbox.move(attacker.x, attacker.y)
        return weapon_hitbox_relative_to_screen.colliderect(target.character_hitbox)
