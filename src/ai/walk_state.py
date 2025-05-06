from math import atan2, pi, sqrt
from random import randrange

from config import ENEMY_ATTACK_INITIATION_DISTANCE, ENEMY_AI_WALK_TIME_MIN, ENEMY_AI_WALK_TIME_MAX
import direction
from direction import Direction
import events
import ai.dying_state   # pylint: disable=cyclic-import
import ai.idle_state   # pylint: disable=cyclic-import
# "State" design pattern is a well-known best practice for implementing game AIs. It often requires
# transitions like state1->state2->state1, and for that reason it is necessary to use cyclic
# imports (like in the example given, state1 would need to import state2 and state2 would also need
# to import state1).
import state

class WalkState(state.State):
    def __init__(self):
        self.__duration = randrange(ENEMY_AI_WALK_TIME_MIN, ENEMY_AI_WALK_TIME_MAX)
        self.__timer = 0
        self.__movement_obstructed = False
        self.__side_movement_direction = "clockwise"

    def enter(self, **kwargs):
        owner = kwargs["owner"]
        opponent = kwargs["opponents"][0]
        other_characters = kwargs["other_characters"]

        owner_bbox = owner.bounding_box
        opponent_bbox = opponent.bounding_box
        angle = atan2(
            owner_bbox.centery - opponent_bbox.centery,
            opponent_bbox.centerx - owner_bbox.centerx
        )
        if -7*pi/8 <= angle < -5*pi/8:
            main_direction = direction.DOWN_LEFT
        elif -5*pi/8 <= angle < -3*pi/8:
            main_direction = direction.DOWN
        elif -3*pi/8 <= angle < -pi/8:
            main_direction = direction.DOWN_RIGHT
        elif -pi/8 <= angle < pi/8:
            main_direction = direction.RIGHT
        elif pi/8 <= angle < 3*pi/8:
            main_direction = direction.UP_RIGHT
        elif 3*pi/8 <= angle < 5*pi/8:
            main_direction = direction.UP
        elif 5*pi/8 <= angle < 7*pi/8:
            main_direction = direction.UP_LEFT
        else:
            main_direction = direction.LEFT

        # If there is an obstacle then try directions +45deg, +90deg, -45deg, -90deg until we find
        # one where there is no obstacle (or if there is an obstacle in every direction tried then
        # we do not move). The directions to try are calculated by multiplying the movement vector
        # with suitable rotation matrices.
        main_x, main_y = main_direction.movement_vector
        directions_to_try = [main_direction]
        clockwise_directions_to_try = [
            Direction(main_x - main_y, main_x + main_y),
            Direction(-main_y, main_x)
        ]
        counterclockwise_directions_to_try = [
            Direction(main_x + main_y, -main_x + main_y),
            Direction(main_y, -main_x)
        ]
        #if self.__side_movement_direction == "clockwise":
        #    directions_to_try += clockwise_directions_to_try + counterclockwise_directions_to_try
        #else:
        #    diretions_to_try += counterclockwise_directions_to_try + clockwise_directions_to_try

        for i in range(len(directions_to_try)):
            if i == 3:
                if self.__side_movement_direction == "clockwise":
                    self.__side_movement_direction = "counterclockwise"
                else:
                    self.__side_movement_direction = "clockwise"

            collides = False
            for character in other_characters:
                if character.state in ("dead", "dying"):
                    continue

                dx, dy = directions_to_try[i].movement_vector

                bbox_moved_horizontally = owner.bounding_box.move(dx, 0)
                collides_horizontally = bbox_moved_horizontally.colliderect(character.bounding_box)

                bbox_moved_vertically = owner.bounding_box.move(0, dy)
                collides_vertically = bbox_moved_vertically.colliderect(character.bounding_box)

                bbox_moved_diagonally = owner.bounding_box.move(dx, dy)
                collides_diagonally = bbox_moved_diagonally.colliderect(character.bounding_box)

                if collides_horizontally or collides_vertically or collides_diagonally:
                    collides = True
                    break

            if not collides:
                owner.direction.moving = directions_to_try[i]
                return

        self.__movement_obstructed = True

    def update(self, **kwargs):
        dt = kwargs["dt"]
        owner = kwargs["owner"]
        opponent = kwargs["opponents"][0]
        other_characters = kwargs["other_characters"]

        if self.__movement_obstructed:
            return ai.idle_state.IdleState()

        self.__timer += dt

        if self.__timer >= self.__duration:
            return ai.idle_state.IdleState()

        owner_bbox = owner.bounding_box
        opponent_bbox = opponent.bounding_box
        dist_x = abs(opponent_bbox.centerx - owner_bbox.centerx)
        dist_y = abs(opponent_bbox.centery - owner_bbox.centery)
        if ((owner_bbox.left <= opponent_bbox.left <= owner_bbox.right or
                owner_bbox.left <= opponent_bbox.right <= owner_bbox.right) and
                (owner_bbox.top <= opponent_bbox.top <= owner_bbox.bottom or
                owner_bbox.top <= opponent_bbox.bottom <= owner_bbox.bottom) or
                sqrt(dist_x ** 2 + dist_y ** 2) <= ENEMY_ATTACK_INITIATION_DISTANCE):
            return ai.idle_state.IdleState()

        for character in other_characters:
            if character.state in ("dead", "dying"):
                continue

            dx, dy = owner.direction.moving.movement_vector

            bbox_moved_horizontally = owner.bounding_box.move(dx, 0)
            collides_horizontally = bbox_moved_horizontally.colliderect(character.bounding_box)

            bbox_moved_vertically = owner.bounding_box.move(0, dy)
            collides_vertically = bbox_moved_vertically.colliderect(character.bounding_box)

            bbox_moved_diagonally = owner.bounding_box.move(dx, dy)
            collides_diagonally = bbox_moved_diagonally.colliderect(character.bounding_box)

            if collides_horizontally or collides_vertically or collides_diagonally:
                return ai.idle_state.IdleState()

    def handle_event(self, **kwargs):
        event = kwargs["event"]

        match event.__class__:
            case events.WasDefeated:
                return ai.dying_state.DyingState()
