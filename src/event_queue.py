import pygame

class EventQueue:
    """Provides a way to get keyboard and mouse input from the user."""

    def get(self):
        """Removes and returns the next input event from the queue.

        Returns:
            The next input event in the queue as a "pygame.event.Event" object.
        """

        return pygame.event.get()
