from direction import direction
from game import events
import states.state

class DyingState(states.state.State):
    def __init__(self, next_state):
        self.__next_state = next_state

    def enter(self, **kwargs):
        owner = kwargs["owner"]

        owner.direction.moving = direction.NONE

    def handle_event(self, **kwargs):
        event = kwargs["event"]

        match event.__class__:
            case events.AnimationFinished:
                return self.__next_state
