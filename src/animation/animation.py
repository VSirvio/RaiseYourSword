class Animation:
    """Stores the framerate and frames of a single animation.

    Attributes:
        framerate: The framerate as an integer.
        frames: A list containing the animation frames.
    """

    def __init__(self, framerate, frames):
        self.framerate = framerate
        self.frames = frames
