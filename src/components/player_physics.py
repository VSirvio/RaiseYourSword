from math import sqrt

class PlayerPhysics:
    def __init__(self, walking_speed, bounding_box, game_area_size):
        game_area_width, game_area_height = game_area_size

        self.__bounding_box = bounding_box

        self.__min_x = -bounding_box.x
        self.__max_x = game_area_width - bounding_box.x - bounding_box.width

        self.__min_y = -bounding_box.y
        self.__max_y = game_area_height - bounding_box.y - bounding_box.height

        self._walk_timer = 0
        self.__walking_speed = walking_speed

    def update(self, dt, player, enemy):
        self._walk_timer += dt

        dx, dy = player.movement_direction.movement_vector

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

            bbox_moved_horizontally = self.bounding_box.move(player.rect.x + dx, player.rect.y)
            collides_horizontally = bbox_moved_horizontally.colliderect(enemy.bounding_box)

            bbox_moved_vertically = self.bounding_box.move(player.rect.x, player.rect.y + dy)
            collides_vertically = bbox_moved_vertically.colliderect(enemy.bounding_box)

            bbox_moved_diagonally = self.bounding_box.move(player.rect.x + dx, player.rect.y + dy)
            collides_diagonally = bbox_moved_diagonally.colliderect(enemy.bounding_box)

            # If diagonal movement causes a collision but horizontal and vertical movement
            # don't (i.e. the corner of the bounding box collides exactly to the corner of the
            # other bounding box), then don't move the player character
            if collides_diagonally and not collides_horizontally and not collides_vertically:
                continue

            if (not collides_horizontally and (dx < 0 and player.rect.x > self.__min_x or
                    dx > 0 and player.rect.x < self.__max_x)):
                player.rect.x += dx

            if (not collides_vertically and (dy < 0 and player.rect.y > self.__min_y or
                    dy > 0 and player.rect.y < self.__max_y)):
                player.rect.y += dy

    @property
    def bounding_box(self):
        return self.__bounding_box
