from direction import direction

class CharacterDirection:
    """Contains the directions a character is facing to and moving to.

    Attributes:
        facing: A Direction object indicating where the character is facing.
    """

    def __init__(self, facing, moving):
        """Creates a new character direction object with the given parameters.

        Args:
            facing: A Direction object indicating where the character is facing.
            moving: A Direction object indicating where the character is moving.
        """

        self.facing = facing
        self.__moving = moving

    @property
    def moving(self):
        """A Direction object indicating where the character is moving."""

        return self.__moving

    @moving.setter
    def moving(self, new_movement_direction):
        """Besides movement direction, sets facing direction correspondingly."""

        self.__moving = new_movement_direction

        if new_movement_direction != direction.NONE:
            self.facing = new_movement_direction.clip_to_four_directions()

    def handle(self, event):
        """A stub for handling game events in subclasses of this class.

        Args:
            event: Event object of one of the classes from the "events" module.
        """
