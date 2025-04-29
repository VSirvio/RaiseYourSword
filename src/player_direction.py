from character_direction import CharacterDirection
import events

class PlayerDirection(CharacterDirection):
    """A CharacterDirection with the "controlled_toward" attribute added to it.

    Attributes:
        controlled_toward: Direction where the character is controlled to.
    """

    def __init__(self, facing, moving, controlled_toward):
        """Creates a new player direction object with the given parameters.

        Args:
            facing: Direction where the character is facing to.
            moving: Direction where the character is moving to.
            controlled_toward: Direction where the character is controlled to.
        """

        super().__init__(facing, moving)
        self.controlled_toward = controlled_toward

    def handle(self, event):
        """Handles a game event.

        Args:
            event: Event object of one of the classes from the "events" module.
        """

        if event.__class__ == events.MovementDirectionChanged:
            self.controlled_toward = event.new_direction
