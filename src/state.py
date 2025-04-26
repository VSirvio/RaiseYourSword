class State:
    @property
    def type(self):
        return self.__class__.__name__.removesuffix("State").lower()

    def update(self, **kwargs):
        return None
