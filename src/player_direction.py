from character_direction import CharacterDirection

class PlayerDirection(CharacterDirection):
    def __init__(self, facing, moving, controlled_toward):
        super().__init__(facing, moving)
        self.controlled_toward = controlled_toward
