import animation

class AttackAnimation(animation.Animation):
    def __init__(self, framerate, damage_frames, frames):
        super().__init__(framerate, frames)
        self.damage_frames = damage_frames
