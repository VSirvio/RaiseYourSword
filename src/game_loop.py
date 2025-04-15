import pygame

from arrow_keys import ArrowKeys

class GameLoop:
    def __init__(self, game, renderer, event_queue, clock):
        self.__game = game
        self.__renderer = renderer
        self.__event_queue = event_queue
        self.__clock = clock

        self.__dt = 0

        self.__arrow_keys = ArrowKeys()

    def start(self):
        while True:
            if not self.__handle_events():
                break

            self.__update()

            self.__renderer.render()

            self.__dt = self.__clock.tick(60)

    def __handle_events(self):
        for event in self.__event_queue.get():
            if event.type == pygame.QUIT:
                return False

            self.__arrow_keys.handle(event)

            if not self.__game.finished:
                self.__game.handle_input(event, self.__arrow_keys.current_direction)

        return True

    def __update(self):
        self.__game.update(self.__dt)
