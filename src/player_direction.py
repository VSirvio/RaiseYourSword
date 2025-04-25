from character_direction import CharacterDirection
import events

class PlayerDirection(CharacterDirection):
    def __init__(self, facing, moving, controlled_toward):
        super().__init__(facing, moving)
        self.controlled_toward = controlled_toward

    def handle(self, event):
        if event.__class__ == events.MovementDirectionChanged:
            self.controlled_toward = event.new_direction
