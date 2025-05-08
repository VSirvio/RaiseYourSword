import pygame

from arrow_keys import ArrowKeys
import events

class GameLoop:
    """Calls the update methods of the game 60 times in a second."""

    def __init__(self, game, renderer, event_queue, clock):
        """Creates a new game loop that utilizes the given services.

        Args:
            game: The game object.
            renderer: A Renderer instance for rendering the game on the screen.
            event_queue: An EventQueue instance for reading user input.
            clock: A Clock instance for the timing.
        """

        self.__game = game
        self.__renderer = renderer
        self.__event_queue = event_queue
        self.__clock = clock

        self.__dt = 0

        self.__arrow_keys = ArrowKeys()

    def start(self):
        """Runs the game loop.

        Returns:
            A boolean value indicating whether to restart the game after this.
        """

        while True:
            exit_action = self.__handle_events()
            if exit_action == "restart":
                return True
            if exit_action == "exit":
                return False

            self.__update()

            self.__renderer.render()

            self.__dt = self.__clock.tick(60)

    def __handle_events(self):
        for event in self.__event_queue.get():
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

    def __update(self):
        self.__game.update(self.__dt)
