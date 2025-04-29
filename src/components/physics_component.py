from math import sqrt

class PhysicsComponent:
    def __init__(self, walking_speed, bounding_box, weapon_hitbox):
        self.__bounding_box = bounding_box
        self.__weapon_hitbox = weapon_hitbox

        self._walk_timer = 0
        self.__walking_speed = walking_speed

    def update(self, dt, *args):
        owner = args[0]

        self._walk_timer += dt

        dx, dy = owner.direction.moving.movement_vector

        time_per_px = 1000 / self.__walking_speed

        # When the walking direction is diagonal, we have to multiply the time
        # it takes to walk 1 pixel (time_per_px) by sqrt(2) = ~1.1,
        # because the distance moved on the screen per pixel is that much
        # longer (compare the diagonal length of a pixel to the width/height of
        # a pixel)
        if dx != 0 and dy != 0:
            time_per_px *= sqrt(2)

        while self._walk_timer >= time_per_px:
            self._walk_timer -= time_per_px
            self._move(dx, dy, *args)

    def _move(self, dx, dy, *args):
        owner = args[0]

        owner.x += dx
        owner.y += dy

    @property
    def bounding_box(self):
        return self.__bounding_box

    def does_attack_hit(self, attacker, target):
        weapon_hitbox = self.__weapon_hitbox[attacker.direction.facing]
        weapon_hitbox_relative_to_screen = weapon_hitbox.move(attacker.x, attacker.y)
        return weapon_hitbox_relative_to_screen.colliderect(target.bounding_box)
