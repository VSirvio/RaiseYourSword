from .physics_component import PhysicsComponent

class PlayerPhysics(PhysicsComponent):
    def __init__(self, walking_speed, bounding_box, weapon_hitbox, game_area_size):
        super().__init__(walking_speed, bounding_box, weapon_hitbox)

        game_area_width, game_area_height = game_area_size

        self.__min_x = -bounding_box.x
        self.__max_x = game_area_width - bounding_box.x - bounding_box.width

        self.__min_y = -bounding_box.y
        self.__max_y = game_area_height - bounding_box.y - bounding_box.height

    def _move(self, dx, dy, *args):
        player = args[0]
        enemy = args[1]

        bbox_moved_horizontally = self.bounding_box.move(player.x + dx, player.y)
        collides_horizontally = bbox_moved_horizontally.colliderect(enemy.bounding_box)

        bbox_moved_vertically = self.bounding_box.move(player.x, player.y + dy)
        collides_vertically = bbox_moved_vertically.colliderect(enemy.bounding_box)

        bbox_moved_diagonally = self.bounding_box.move(player.x + dx, player.y + dy)
        collides_diagonally = bbox_moved_diagonally.colliderect(enemy.bounding_box)

        # If diagonal movement causes a collision but horizontal and vertical movement
        # don't (i.e. the corner of the bounding box collides exactly to the corner of the
        # other bounding box), then don't move the player character
        if collides_diagonally and not collides_horizontally and not collides_vertically:
            return

        if (not collides_horizontally and (dx < 0 and player.x > self.__min_x or
                dx > 0 and player.x < self.__max_x)):
            player.x += dx

        if (not collides_vertically and (dy < 0 and player.y > self.__min_y or
                dy > 0 and player.y < self.__max_y)):
            player.y += dy
