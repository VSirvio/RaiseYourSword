import direction
import states.idle_state   # pylint: disable=cyclic-import
import states.walk_state   # pylint: disable=cyclic-import
# "State" design pattern is a well-known best practice for implementing animation state management
# in games. It often requires transitions like state1->state2->state1, and for that reason it is
# necessary to use cyclic imports (like in the example given, state1 would need to import state2
# and state2 would also need to import state1).

class AttackState:
    def __init__(self, direction_pressed):
        self.__enemy_was_hit = False
        self.__direction_pressed = direction_pressed

    @property
    def type(self):
        return "attack"

    def enter(self, **kwargs):
        self.__enemy_was_hit = kwargs["player"].attack(kwargs["enemy"])

    def handle_input(self, **kwargs):
        self.__direction_pressed = kwargs["direction_pressed"]

    def animation_finished(self):
        if self.__direction_pressed == direction.NONE:
            return states.idle_state.IdleState()
        return states.walk_state.WalkState(self.__direction_pressed)

    def has_been_defeated(self):
        return states.idle_state.IdleState()

    @property
    def enemy_was_hit(self):
        return self.__enemy_was_hit
