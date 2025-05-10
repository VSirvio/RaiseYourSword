class AiConfig:
    def __init__(self, idle_time, walk_time, attack_initiation_distance):
        self.__idle_time = idle_time
        self.__walk_time = walk_time
        self.__attack_initiation_distance = attack_initiation_distance

    @property
    def idle_time(self):
        return self.__idle_time

    @property
    def walk_time(self):
        return self.__walk_time

    @property
    def attack_initiation_distance(self):
        return self.__attack_initiation_distance
