class State:
    @property
    def type(self):
        return self.__class__.__name__.removesuffix("State").lower()

    def update(self, **kwargs):
        if "dt" not in kwargs:
            raise TypeError("State.update() requires keyword argument \"dt\"")

    def handle_event(self, **kwargs):
        if "event" not in kwargs:
            raise TypeError("State.handle_event() requires keyword argument \"event\"")
