import direction
import state

class PerpetualIdleState(state.State):
    @property
    def type(self):
        return "idle"

    def enter(self, **kwargs):
        owner = kwargs["owner"]

        owner.direction.moving = direction.NONE
