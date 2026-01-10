class GameLoop:
    """Calls the update methods of the game at regular intervals."""

    def __init__(self, game, framerate, renderer, event_queue, input_handler, clock):
        """Creates a new game loop that utilizes the given services.

        Args:
            game: The game object.
            framerate: The number of times the game loop should be run per second.
            renderer: A Renderer instance for rendering the game on the screen.
            event_queue: An EventQueue instance for reading user input.
            input_handler: An InputHandler instance for processing input events.
            clock: A Clock instance for the timing.
        """

        self.__game = game
        self.__framerate = framerate
        self.__renderer = renderer
        self.__event_queue = event_queue
        self.__input_handler = input_handler
        self.__clock = clock

        self.__dt = 0

    def start(self):
        """Runs the game loop.

        Returns:
            A boolean value indicating whether to restart the game after this.
        """

        while True:
            exit_action = self.__input_handler.handle_events(self.__event_queue)

            if exit_action == "restart":
                return True
            elif exit_action == "exit":
                return False

            self.__game.update(self.__dt)

            self.__renderer.render()

            self.__dt = self.__clock.tick(self.__framerate)
