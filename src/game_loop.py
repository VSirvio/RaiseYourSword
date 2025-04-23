import pygame

from arrow_keys import ArrowKeys
import events

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

            direction_changed = self.__arrow_keys.handle(event)

            if not self.__game.finished:
                if direction_changed:
                    new_direction = self.__arrow_keys.current_direction
                    self.__game.handle(events.MovementDirectionChanged(new_direction))
                elif (event.type == pygame.KEYDOWN and
                        event.key in (pygame.K_RSHIFT, pygame.K_LSHIFT)):
                    self.__game.handle(events.AttackStarted())

        return True

    def __update(self):
        self.__game.update(self.__dt)
