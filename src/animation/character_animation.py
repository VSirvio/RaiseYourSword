class CharacterAnimation:
    """Stores all the animation sets of a character.

    Attributes:
        sprite_sheet: A pygame Surface that contains all the animation frames.
        frame_width: The width of a single animation frame in pixels.
        frame_height: The height of a single animation frame in pixels.
    """

    def __init__(self, sprite_sheet, frame_width, frame_height, animation_sets):
        """Creates a character animation with the given parameters.

        Args:
            sprite_sheet: A pygame Surface that contains the animation frames.
            frame_width: An integer.
            frame_height: An integer.
            animation_sets: A dict with "the set name as string"->AnimationSet.
        """

        self.sprite_sheet = sprite_sheet
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.__animation_sets = animation_sets

    def __getitem__(self, animation_set_name):
        """Fetches an animation set by name.

        Args:
            animation_set_name: The name of the animation set as a string.

        Returns:
            An AnimationSet instance corresponding to the given name.
        """

        return self.__animation_sets[animation_set_name]
