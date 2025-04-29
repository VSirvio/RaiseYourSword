class State:
    """A state in finite state machine used for character state transitions."""

    @property
    def type(self):
        """A string indicating the type of the state (e.g. "walk", "attack")."""

        return self.__class__.__name__.removesuffix("State").lower()

    def update(self, **kwargs):
        """A stub for handling updating the state in subclasses of this class.

        Args:
            dt: Elapsed time since the last call of this method in milliseconds.
        """

        if "dt" not in kwargs:
            raise TypeError("State.update() requires keyword argument \"dt\"")

    def handle_event(self, **kwargs):
        """A stub for handling game events in subclasses of this class.

        Args:
            event: Event object of one of the classes from the "events" module.
        """

        if "event" not in kwargs:
            raise TypeError("State.handle_event() requires keyword argument \"event\"")
