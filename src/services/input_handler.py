import pygame

from game import events
from game.arrow_keys import ArrowKeys

class InputHandler:
    """Reads Pygame events from the event queue and handles them."""

    def __init__(self, game):
        """Creates an input handler for the game object.

        Args:
            game: The game object.
        """

        self.__game = game

        self.__arrow_keys = ArrowKeys()

    def handle_events(self, event_queue):
        """Reads events from the event queue and relays them to the game.

        Args:
            event_queue: An EventQueue instance for reading user input.

        Returns:
            The string "exit", "restart" or "continue".
        """

        for event in event_queue.get():
            if (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE or
                    event.type == pygame.QUIT):
                return "exit"

            direction_changed = self.__arrow_keys.handle(event)

            if direction_changed:
                new_direction = self.__arrow_keys.current_direction
                self.__game.handle(events.MovementDirectionChanged(new_direction))
            elif (event.type == pygame.KEYDOWN and
                    event.key in (pygame.K_RSHIFT, pygame.K_LSHIFT, pygame.K_SPACE, pygame.K_x)):
                self.__game.handle(events.AttackStarted())
            elif (event.type == pygame.KEYUP and event.key in (pygame.K_LSHIFT, pygame.K_RETURN,
                    pygame.K_RSHIFT, pygame.K_SPACE, pygame.K_x, pygame.K_z)):
                self.__game.handle(events.Accept())

            if (self.__game.finished and event.type == pygame.KEYUP and
                    event.key in (pygame.K_SPACE, pygame.K_RETURN)):
                return "restart"

        return "continue"
