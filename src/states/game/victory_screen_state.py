import os

import pygame

import states.game.ending_screen_state

dirname = os.path.dirname(__file__)

class VictoryScreenState(states.game.ending_screen_state.EndingScreenState):
    """Game state for the ending screen shown after victory."""

    def __init__(self):
        super().__init__(
            message_image=pygame.image.load(
                os.path.join(dirname, "..", "..", "assets", "victory_message.png")
            ),
            message_position=(36, 90),
            instructions_image=pygame.image.load(
                os.path.join(dirname, "..", "..", "assets", "victory_instructions.png")
            ),
            instructions_position=(36, 167)
        )
