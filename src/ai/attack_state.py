import ai.dying_state   # pylint: disable=cyclic-import
import ai.idle_state   # pylint: disable=cyclic-import
# "State" design pattern is a well-known best practice for implementing game AIs. It often requires
# transitions like state1->state2->state1, and for that reason it is necessary to use cyclic
# imports (like in the example given, state1 would need to import state2 and state2 would also need
# to import state1).
from direction import NONE, DOWN, UP, RIGHT, LEFT
import events
import state

class AttackState(state.State):
    def enter(self, **kwargs):
        owner = kwargs["owner"]
        opponent = kwargs["opponents"][0]

        owner_bbox = owner.bounding_box
        opponent_bbox = opponent.bounding_box
        if owner_bbox.bottom <= opponent_bbox.top and owner_bbox.right > opponent_bbox.left:
            owner.direction.moving = DOWN
        elif owner_bbox.left >= opponent_bbox.right and owner_bbox.bottom > opponent_bbox.top:
            owner.direction.moving = LEFT
        elif owner_bbox.top >= opponent_bbox.bottom and owner_bbox.left < opponent_bbox.right:
            owner.direction.moving = UP
        else:
            owner.direction.moving = RIGHT

        owner.direction.moving = NONE

    def handle_event(self, **kwargs):
        event = kwargs["event"]
        owner = kwargs["owner"] if event.__class__ == events.DealingDamage else None
        opponent = kwargs["opponents"][0] if event.__class__ == events.DealingDamage else None

        match event.__class__:
            case events.AnimationFinished:
                return ai.idle_state.IdleState()
            case events.DealingDamage:
                if owner.does_attack_hit(opponent):
                    #opponent.defeat()
                    pass
            case events.WasDefeated:
                return ai.dying_state.DyingState()
