class Range:
    """Stores the minimum and maximum values of a range."""

    def __init__(self, minimum, maximum):
        """Create a range with the given minimum and maximum values.

        Args:
            minimum: The smallest integer value included in the range.
            maximum: The largest integer value included in the range.
        """

        self.__minimum = minimum
        self.__maximum = maximum

    @property
    def minimum(self):
        """The smallest integer value included in this range."""

        return self.__minimum

    @property
    def maximum(self):
        """The largest integer value included in this range."""

        return self.__maximum
