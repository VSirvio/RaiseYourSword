class CharacterAnimation:
    def __init__(self, sprite_sheet, frame_width, frame_height, animation_sets):
        self.sprite_sheet = sprite_sheet
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.__animation_sets = animation_sets

    def __getitem__(self, animation_set_name):
        return self.__animation_sets[animation_set_name]
