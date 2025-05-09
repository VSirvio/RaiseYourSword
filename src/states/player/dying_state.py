import states.player.dead_state   # pylint: disable=cyclic-import
# "State" design pattern is a well-known best practice for implementing animation state management
# in games. It often requires transitions like state1->state2->state1, and for that reason it is
# necessary to use cyclic imports (like in the example given, state1 would need to import state2
# and state2 would also need to import state1).
import states.dying_state

class DyingState(states.dying_state.DyingState):
    def __init__(self):
        super().__init__(next_state=states.player.dead_state.DeadState())
