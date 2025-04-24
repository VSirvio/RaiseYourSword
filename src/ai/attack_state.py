import ai.idle_state   # pylint: disable=cyclic-import
# "State" design pattern is a well-known best practice for implementing game AIs. It often requires
# transitions like state1->state2->state1, and for that reason it is necessary to use cyclic
# imports (like in the example given, state1 would need to import state2 and state2 would also need
# to import state1).
import state

class AttackState(state.State):
    def __init__(self):
        self.__player_was_hit = False

    def enter(self, **kwargs):
        self.__player_was_hit = kwargs["enemy"].attack(kwargs["player"])

    def update(self, **kwargs):
        return None

    def animation_finished(self):
        return ai.idle_state.IdleState(game_finished=self.__player_was_hit)

    @property
    def player_was_hit(self):
        return self.__player_was_hit
