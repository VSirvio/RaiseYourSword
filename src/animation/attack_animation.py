from .animation import Animation

class AttackAnimation(Animation):
    """A sub class of Animation class that also contains damage frame data.

    Attributes:
        framerate: The framerate as an integer.
        frames: A list containing the animation frames.
        damage_frames: Indexes of the frames during which damage is inflicted.
    """

    def __init__(self, framerate, damage_frames, frames):
        super().__init__(framerate, frames)
        self.damage_frames = damage_frames
