import os

import pygame

import states.game.ending_screen_state

dirname = os.path.dirname(__file__)

class DefeatScreenState(states.game.ending_screen_state.EndingScreenState):
    def __init__(self):
        super().__init__(
            message_image=pygame.image.load(
                os.path.join(dirname, "..", "..", "assets", "defeat_message.png")
            ),
            message_position=(38, 90),
            instructions_image=pygame.image.load(
                os.path.join(dirname, "..", "..", "assets", "defeat_instructions.png")
            ),
            instructions_position=(55, 170)
        )
