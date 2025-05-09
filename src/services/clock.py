import pygame

class Clock:
    """Provides the capability to run a task regularly."""

    def __init__(self):
        self.__clock = pygame.time.Clock()

    def tick(self, execution_rate):
        """Waits until it is time to run the task again.

        Args:
            execution_rate: The number of times the task should be run in 1 s.

        Returns:
            The number of milliseconds passed since the previous call.
        """

        return self.__clock.tick(execution_rate)
